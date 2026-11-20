# -*- coding: utf-8 -*-
"""
Big 4 Accounting Firms News Aggregator & Crawler
Google News RSS 및 주요 언론사 뉴스 피드 파싱 모듈
"""

import os
import re
import json
import hashlib
import logging
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from bs4 import BeautifulSoup

from sample_data import SAMPLE_NEWS, FIRMS_INFO

logger = logging.getLogger(__name__)

# 인메모리 캐시 (파일시스템 실패 시에도 100% 안전하게 동작)
_MEMORY_CACHE = None

# Vercel / Lambda 환경 감지
IS_VERCEL = bool(os.environ.get("VERCEL") or os.environ.get("VERCEL_ENV") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))
if IS_VERCEL:
    CACHE_DIR = "/tmp"
    CACHE_FILE = "/tmp/big4_news_cache.json"
else:
    CACHE_DIR = os.path.join(os.path.dirname(__file__), "data")
    CACHE_FILE = os.path.join(CACHE_DIR, "news_cache.json")

# 수집 대상 쿼리 및 법인 매핑
CRAWL_TARGETS = [
    {"firm": "samil", "query": '"삼일PwC" OR "삼일회계법인"'},
    {"firm": "samjong", "query": '"삼정KPMG" OR "삼정회계법인"'},
    {"firm": "ey", "query": '"EY한영" OR "한영회계법인"'},
    {"firm": "deloitte", "query": '"딜로이트 안진" OR "안진회계법인"'},
    {"firm": "all", "query": '"빅4 회계법인" OR "4대 회계법인"'}
]

# 모든 기사 시각은 한국 표준시(KST)로 통일해 저장/정렬한다.
KST = timezone(timedelta(hours=9))
MAX_CACHED_ITEMS = 300   # 캐시가 무한정 커지지 않도록 최신 기사만 보관
FETCH_TIMEOUT = 5        # 피드 1건당 타임아웃(초). 병렬 수집이라 전체도 약 5초 이내 (Vercel 10초 제한 대응)


def now_kst():
    return datetime.now(KST)


def parse_pub_date(value):
    """발행일 문자열을 시간대 있는 datetime으로 변환 (정렬용).
    시간대가 없으면 KST로 간주하고, 해석 불가 시 가장 오래된 값을 반환한다."""
    if not value:
        return datetime.min.replace(tzinfo=timezone.utc)
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        try:
            dt = parsedate_to_datetime(str(value))
        except Exception:
            return datetime.min.replace(tzinfo=timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=KST)
    return dt


def pub_date_sort_key(item):
    return parse_pub_date(item.get("pub_date"))


def init_cache():
    """초기 캐시 준비"""
    global _MEMORY_CACHE
    if _MEMORY_CACHE is None:
        _MEMORY_CACHE = list(SAMPLE_NEWS)
    try:
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR, exist_ok=True)
        if not os.path.exists(CACHE_FILE):
            save_news_cache(_MEMORY_CACHE)
    except Exception as e:
        logger.warning(f"Cache init warning (continuing with in-memory): {e}")

def load_news_cache():
    """캐시에서 뉴스 로드 (메모리 캐시 우선 및 절대 실패 방지)"""
    global _MEMORY_CACHE
    if _MEMORY_CACHE:
        return _MEMORY_CACHE
        
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                news = json.load(f)
                if news:
                    _MEMORY_CACHE = news
                    return _MEMORY_CACHE
    except Exception as e:
        logger.warning(f"Cache read failed (using sample_data): {e}")
        
    _MEMORY_CACHE = list(SAMPLE_NEWS)
    return _MEMORY_CACHE

def save_news_cache(news_list):
    """뉴스 목록을 메모리 및 캐시 파일에 저장"""
    global _MEMORY_CACHE
    _MEMORY_CACHE = list(news_list)
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(news_list, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.warning(f"Failed to save file cache (in-memory updated): {e}")

# 법인별 식별 패턴 (대소문자 무시, 영문 약칭은 단어 경계 적용)
FIRM_PATTERNS = {
    "samil": re.compile(r"삼일(?!절)|(?<![a-z])pwc(?![a-z])", re.IGNORECASE),
    "samjong": re.compile(r"삼정|(?<![a-z])kpmg(?![a-z])", re.IGNORECASE),
    "ey": re.compile(r"한영|(?<![a-z])ey(?![a-z])|ernst\s*&\s*young", re.IGNORECASE),
    "deloitte": re.compile(r"안진|딜로이트|(?<![a-z])deloitte(?![a-z])", re.IGNORECASE),
}


def detect_firm_ids(text):
    """텍스트에서 언급된 회계법인 id 목록 반환"""
    text = text or ""
    return [firm_id for firm_id, pattern in FIRM_PATTERNS.items() if pattern.search(text)]


def item_matches_firm(item, firm):
    """기사가 특정 법인 기사인지 판정. 목록/집계/CSV가 모두 이 함수를 공유한다."""
    if not firm or firm == "all":
        return True
    if item.get("firm") == firm:
        return True
    return firm in detect_firm_ids((item.get("title") or "") + " " + (item.get("summary") or ""))


def detect_firms(text):
    """기사 텍스트에서 언급된 회계법인 식별 (여러 법인이면 'all')"""
    matched = detect_firm_ids(text)
    return matched[0] if len(matched) == 1 else "all"

CATEGORY_RULES = [
    ("감사/회계", ["감사", "회계", "지정제", "감사인", "감사품질", "결산", "분식회계", "내부회계"]),
    ("세무/택스", ["세무", "조세", "국세청", "법인세", "최저한세", "상속세", "이전가격", "택스"]),
    ("M&A/자문", ["m&a", "인수합병", "매각", "실사", "재무자문", "투자유치", "pef", "지분 인수"]),
    ("컨설팅/거버넌스", ["ai", "인공지능", "생성형", "dx", "디지털", "컨설팅", "로봇", "솔루션", "클라우드"]),
    ("ESG/사회공헌", ["esg", "탄소", "기후", "사회공헌", "기부", "봉사", "장학", "친환경"]),
    ("인사/동정", ["인사", "선임", "파트너", "대표이사", "채용", "cpa", "합격자", "동정"]),
    ("경영실적", ["실적", "매출", "영업이익", "성장", "경영성과"]),
]


def _contains_word(text, word):
    """영문/숫자 키워드는 단어 경계로, 한글 키워드는 부분 문자열로 검사.
    (예: 'ai'가 'maintain'에, 'dx'가 다른 영단어에 걸리는 오분류 방지)"""
    if word.isascii():
        return re.search(r"(?<![a-z0-9])" + re.escape(word) + r"(?![a-z0-9])", text) is not None
    return word in text


def categorize_news(title, content):
    """기사 내용 기반 카테고리 자동 추론"""
    full_text = (title + " " + content).lower()
    # '회계법인'이라는 회사명 자체가 '회계'로 잡히거나, '인사이트'가 '인사'로 잡히는 것을 방지
    full_text = full_text.replace("회계법인", " ").replace("인사이트", " ")

    for category, words in CATEGORY_RULES:
        if any(_contains_word(full_text, w) for w in words):
            return category
    return "일반/경영"

def extract_tags(title, content):
    """주요 키워드 해시태그 추출"""
    full_text = title + " " + content
    candidates = [
        "생성형AI", "AI에이전트", "디지털전환", "회계감사", "감사품질",
        "주기적지정제", "M&A", "재무자문", "기업인수", "글로벌최저한세",
        "세무조사", "국제조세", "ESG", "기후공시", "지속가능경영",
        "내부회계관리", "공인회계사", "CPA채용", "신임파트너", "사외이사"
    ]
    found = [tag for tag in candidates if tag.lower() in full_text.lower()]
    return found[:4] if found else ["회계법인", "빅4", "경영이슈"]

def clean_html(raw_html):
    """HTML 태그 제거 및 텍스트 정제"""
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text)
    return text

def parse_rss_feed(url, default_firm="all"):
    """Google News RSS 피드를 읽어 뉴스 아이템 파싱"""
    items = []
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )
    with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as response:
        xml_data = response.read()
        root = ET.fromstring(xml_data)
        
        for item in root.findall(".//item"):
            title_el = item.find("title")
            link_el = item.find("link")
            pub_date_el = item.find("pubDate")
            desc_el = item.find("description")
            source_el = item.find("source")
            
            raw_title = title_el.text if title_el is not None and title_el.text else ""
            link = link_el.text if link_el is not None and link_el.text else ""
            raw_pub_date = pub_date_el.text if pub_date_el is not None else ""
            raw_desc = desc_el.text if desc_el is not None else ""
            source_name = source_el.text if source_el is not None and source_el.text else ""
            
            # 구글 뉴스 제목 포맷: '기사 제목 - 언론사'
            title = raw_title
            if " - " in raw_title:
                parts = raw_title.rsplit(" - ", 1)
                title = parts[0].strip()
                if not source_name:
                    source_name = parts[1].strip()
            
            if not source_name:
                source_name = "종합뉴스"
                
            clean_desc = clean_html(raw_desc)
            # 불필요한 언론사명 반복 제거
            clean_desc = clean_desc.replace(source_name, "").strip()
            if len(clean_desc) < 15:
                clean_desc = f"{title} 관련 상세 보도 내용입니다."
                
            # 날짜 파싱
            pub_date_iso = now_kst().isoformat()
            if raw_pub_date:
                try:
                    dt = parsedate_to_datetime(raw_pub_date)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    pub_date_iso = dt.astimezone(KST).isoformat()
                except Exception:
                    pass
                    
            firm_key = detect_firms(title + " " + clean_desc)
            if firm_key == "all" and default_firm != "all":
                firm_key = default_firm
                
            firm_info = FIRMS_INFO.get(firm_key, FIRMS_INFO["all"])
            category = categorize_news(title, clean_desc)
            tags = extract_tags(title, clean_desc)
            
            item_id = hashlib.md5((link or title).encode("utf-8")).hexdigest()[:12]
            
            items.append({
                "id": f"crawl-{item_id}",
                "title": title,
                "firm": firm_key,
                "firm_name": firm_info["name"],
                "source": source_name,
                "author": f"{source_name} 기자",
                "pub_date": pub_date_iso,
                "summary": clean_desc[:220] + ("..." if len(clean_desc) > 220 else ""),
                "url": link,
                "category": category,
                "tags": tags
            })
    return items

def _crawl_target(target):
    firm = target["firm"]
    encoded_query = urllib.parse.quote(target["query"])
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
    try:
        return firm, parse_rss_feed(rss_url, default_firm=firm), None
    except Exception as e:
        return firm, [], f"Target '{firm}' query failed: {e}"


def fetch_live_news():
    """모든 타겟에 대해 실시간 뉴스 크롤링 수행 (병렬 — 서버리스 시간 제한 대응)"""
    all_crawled = []
    errors = []

    with ThreadPoolExecutor(max_workers=len(CRAWL_TARGETS)) as pool:
        for _firm, items, error in pool.map(_crawl_target, CRAWL_TARGETS):
            all_crawled.extend(items)
            if error:
                errors.append(error)

    # 기존 캐시 및 샘플 데이터와 중복 제거 병합
    cached_news = load_news_cache()

    # 고유성 기준: 제목 정규화
    seen_titles = set()
    merged = []

    # 실시간 크롤링 기사 우선 추가, 이후 기존 캐시/샘플 보강
    for item in all_crawled + cached_news:
        norm_title = re.sub(r"[\s\W_]+", "", item.get("title", "")).lower()
        if norm_title and norm_title not in seen_titles:
            seen_titles.add(norm_title)
            merged.append(item)

    # 시간대가 섞여 있어도 올바르게 최신순 정렬 후, 오래된 기사는 잘라낸다
    merged.sort(key=pub_date_sort_key, reverse=True)
    merged = merged[:MAX_CACHED_ITEMS]

    # 수집이 전부 실패했다면 캐시를 덮어쓰지 않는다
    if all_crawled:
        save_news_cache(merged)

    return {
        # 모든 피드가 실패했다면 성공으로 보고하지 않는다 (화면에 '수집 완료'로 오해되지 않도록)
        "success": bool(all_crawled) or not errors,
        "total": len(merged),
        "crawled_count": len(all_crawled),
        "errors": errors
    }

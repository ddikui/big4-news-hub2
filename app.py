# -*- coding: utf-8 -*-
"""
Big 4 Accounting Firms News Hub - Backend Server
Flask RESTful Web Application (Vercel Serverless 호환)
"""

import io
import csv
import os
from urllib.parse import parse_qsl, urlencode
from datetime import datetime
from flask import Flask, render_template, request, jsonify, Response

from sample_data import FIRMS_INFO
from crawler import (
    load_news_cache,
    fetch_live_news,
    init_cache,
    item_matches_firm,
    pub_date_sort_key,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 정적 파일은 public/static 한 곳에서만 관리한다.
# (Vercel은 public/ 을 CDN으로 서빙하고, 로컬 Flask도 같은 폴더를 사용하므로
#  로컬에서 고친 내용이 배포 환경과 어긋나지 않는다.)
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "public", "static"),
    static_url_path="/static"
)
app.config["JSON_AS_ASCII"] = False

# 초기 캐시 확인 및 로드
init_cache()

# 캐시에 샘플 데이터만 있는 상태라면 최초 1회 실시간 수집 수행
_initial_items = load_news_cache()
if _initial_items and all(not str(it.get("id", "")).startswith("crawl-") for it in _initial_items):
    try:
        fetch_live_news()
    except Exception:
        pass

API_ROUTES = {"news", "firms", "stats", "refresh", "export"}


class ApiRouteMiddleware:
    """`/api/index?__route=news&limit=2` 형태의 요청을 `/api/news?limit=2` 로 바꿔 준다.

    Vercel 에서 rewrite 로 /api/news 같은 하위 경로를 함수(api/index.py)에 넘기면
    경로가 보존되지 않아 모든 API 가 대시보드 HTML 로 응답되는 문제가 있었다.
    그래서 프런트엔드는 항상 함수 파일 주소(/api/index)로 호출하고, 실제 엔드포인트는
    쿼리스트링(__route)으로 전달한다. 쿼리스트링은 어떤 환경에서도 그대로 전달된다.
    (로컬 Flask 실행에서도 동일하게 동작한다.)
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        # PATH_INFO 가 무엇으로 들어오든(/api/index, /, ...) __route 가 있으면 그것을 따른다.
        params = parse_qsl(environ.get("QUERY_STRING", ""), keep_blank_values=True)
        route = next((v for k, v in params if k == "__route"), None)
        if route in API_ROUTES:
            environ["PATH_INFO"] = "/api/" + route
            environ["QUERY_STRING"] = urlencode([(k, v) for k, v in params if k != "__route"])
        return self.wsgi_app(environ, start_response)


app.wsgi_app = ApiRouteMiddleware(app.wsgi_app)

MAX_PAGE_SIZE = 50
MAX_IDS_PAGE_SIZE = 200  # 스크랩(ids) 조회 시 허용하는 최대 개수


@app.route("/")
@app.route("/index")
@app.route("/api/index")
@app.route("/api/index.py")
def index():
    """메인 대시보드 페이지"""
    return render_template("index.html", firms_info=FIRMS_INFO)


def parse_filters(args):
    """쿼리 파라미터를 필터 dict로 정리"""
    ids_param = args.get("ids")
    return {
        "firm": args.get("firm", "all").strip().lower(),
        "source": args.get("source", "").strip(),
        "category": args.get("category", "").strip(),
        "query": args.get("q", "").strip().lower(),
        "ids": {i.strip() for i in ids_param.split(",") if i.strip()} if ids_param is not None else None,
    }


def apply_filters(news, filters, skip=()):
    """뉴스 목록에 필터를 적용. skip에 넣은 필터 이름은 건너뛴다(패싯 집계용)."""
    result = news

    if "firm" not in skip and filters["firm"] and filters["firm"] != "all":
        result = [item for item in result if item_matches_firm(item, filters["firm"])]

    if "source" not in skip and filters["source"]:
        result = [item for item in result if item.get("source") == filters["source"]]

    if "category" not in skip and filters["category"]:
        result = [item for item in result if item.get("category") == filters["category"]]

    if "query" not in skip and filters["query"]:
        q = filters["query"]
        result = [
            item for item in result
            if q in item.get("title", "").lower()
            or q in item.get("summary", "").lower()
            or any(q in tag.lower() for tag in item.get("tags", []))
            or q in item.get("source", "").lower()
        ]

    if "ids" not in skip and filters["ids"] is not None:
        result = [item for item in result if item.get("id") in filters["ids"]]

    return result


def sort_news(news, sort_by):
    if sort_by == "title":
        return sorted(news, key=lambda x: x.get("title", ""))
    return sorted(news, key=pub_date_sort_key, reverse=True)  # latest (기본값)


def count_by(news, field, default):
    counts = {}
    for item in news:
        key = item.get(field, default)
        counts[key] = counts.get(key, 0) + 1
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)


@app.route("/api/firms", methods=["GET"])
def get_firms():
    """회계법인 메타데이터 및 각 법인별 기사 수 카운트 반환
    (기사 수는 뉴스 목록 API와 같은 판정 기준을 사용)"""
    all_news = load_news_cache()

    firms_data = []
    for firm_id, info in FIRMS_INFO.items():
        data = dict(info)
        data["news_count"] = sum(1 for item in all_news if item_matches_firm(item, firm_id))
        firms_data.append(data)

    return jsonify({
        "success": True,
        "firms": firms_data
    })


@app.route("/api/news", methods=["GET"])
def get_news():
    """뉴스 목록 필터링, 검색, 정렬 및 페이지네이션 API"""
    all_news = load_news_cache()

    filters = parse_filters(request.args)
    sort_by = request.args.get("sort", "latest")
    max_limit = MAX_IDS_PAGE_SIZE if filters["ids"] is not None else MAX_PAGE_SIZE

    try:
        page = max(1, int(request.args.get("page", 1)))
        limit = min(max_limit, max(1, int(request.args.get("limit", 12))))
    except ValueError:
        page, limit = 1, 12

    filtered = sort_news(apply_filters(all_news, filters), sort_by)

    # 패싯(언론사/카테고리) 집계: 자기 자신의 필터는 제외하고 계산해야
    # 언론사를 하나 골라도 다른 언론사 선택지가 사라지지 않는다.
    source_facet = count_by(apply_filters(all_news, filters, skip=("source",)), "source", "기타")
    category_facet = count_by(apply_filters(all_news, filters, skip=("category",)), "category", "일반/경영")

    total = len(filtered)
    total_pages = (total + limit - 1) // limit if total > 0 else 1

    start_idx = (page - 1) * limit
    paginated_news = filtered[start_idx:start_idx + limit]

    # 샘플 데이터처럼 언론사 메인 도메인만 있는 경우 기사 제목 검색 원문 링크로 보정
    fixed_news = []
    for item in paginated_news:
        copy_item = dict(item)
        u = copy_item.get("url", "")
        if u and u.rstrip("/").count("/") == 2 and copy_item.get("title"):
            q = urlencode({"where": "news", "query": copy_item["title"]})
            copy_item["url"] = f"https://search.naver.com/search.naver?{q}"
        fixed_news.append(copy_item)

    return jsonify({
        "success": True,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "news": fixed_news,
        "facets": {
            "sources": source_facet,
            "categories": category_facet
        }
    })


@app.route("/api/refresh", methods=["POST"])
def refresh_news():
    """실시간 뉴스 크롤링 수행"""
    try:
        return jsonify(fetch_live_news())
    except Exception as e:  # 예기치 못한 오류도 JSON으로 응답해 프런트가 처리할 수 있게 한다
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """대시보드 시각화용 통계 데이터 반환"""
    all_news = load_news_cache()

    # 1. 회계법인별 기사 점유율
    firm_counts = {"samil": 0, "samjong": 0, "ey": 0, "deloitte": 0, "all": 0}
    for item in all_news:
        f = item.get("firm", "all")
        if f in firm_counts:
            firm_counts[f] += 1

    firm_labels = {
        "samil": "삼일 PwC",
        "samjong": "삼정 KPMG",
        "ey": "한영 EY",
        "deloitte": "안진 Deloitte",
        "all": "공통/업계전반"
    }

    # 2. 카테고리별 비중
    cat_counts = {}
    for item in all_news:
        cat = item.get("category", "기타")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    # 3. 주요 언론사 Top 6
    top_sources = count_by(all_news, "source", "기타")[:6]

    # 4. 인기 태그 Top 10
    tag_counts = {}
    for item in all_news:
        for tag in item.get("tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    return jsonify({
        "success": True,
        "firms_distribution": {
            "labels": [firm_labels[k] for k in ["samil", "samjong", "ey", "deloitte", "all"]],
            "data": [firm_counts[k] for k in ["samil", "samjong", "ey", "deloitte", "all"]],
            "colors": ["#e05307", "#0051C7", "#E5A900", "#007624", "#64748b"]
        },
        "categories_distribution": {
            "labels": list(cat_counts.keys()),
            "data": list(cat_counts.values())
        },
        "top_sources": {
            "labels": [x[0] for x in top_sources],
            "data": [x[1] for x in top_sources]
        },
        "top_tags": top_tags,
        "total_news": len(all_news)
    })


def csv_safe(value):
    """엑셀 수식 주입 방지: =, +, -, @ 로 시작하는 셀은 앞에 ' 를 붙인다"""
    text = "" if value is None else str(value)
    return "'" + text if text[:1] in ("=", "+", "-", "@") else text


@app.route("/api/export", methods=["GET"])
def export_news():
    """현재 화면 조건(법인/언론사/분야/검색어/정렬)과 같은 기준으로 CSV 내보내기"""
    all_news = load_news_cache()
    filters = parse_filters(request.args)
    rows = sort_news(apply_filters(all_news, filters), request.args.get("sort", "latest"))

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "회계법인", "언론사", "기사제목", "작성자", "발행일시", "카테고리", "태그", "기사요약", "원문URL"])

    for item in rows:
        writer.writerow([csv_safe(v) for v in [
            item.get("id", ""),
            item.get("firm_name", ""),
            item.get("source", ""),
            item.get("title", ""),
            item.get("author", ""),
            item.get("pub_date", ""),
            item.get("category", ""),
            ", ".join(item.get("tags", [])),
            item.get("summary", ""),
            item.get("url", "")
        ]])

    csv_data = "﻿" + output.getvalue()  # Excel 한글 깨짐 방지 BOM 추가
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=big4_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

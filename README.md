# 🏢 BIG4 NEWS HUB (빅4 회계법인 전문 뉴스 인텔리전스)

대한민국 빅4 회계법인(**삼일 PwC, 삼정 KPMG, 한영 EY, 안진 Deloitte**) 관련 주요 뉴스를 다양한 언론사에서 실시간으로 수집하고, 전체 또는 특정 회계법인별로 분류하여 확인할 수 있는 웹 애플리케이션입니다.

---

## ✨ 핵심 기능

1. **🏢 전체 및 특정 회계법인별 뉴스 필터링**
   - **전체 빅4 (Big 4 Korea)**: 4대 회계법인 통합 뉴스피드 및 업계 종합 이슈
   - **🔴 삼일 PwC (Samil PwC)**: 회계감사, M&A 딜자문, 세무, AI 혁신 뉴스
   - **🔵 삼정 KPMG (Samjong KPMG)**: 산업 전망 리포트, 금융·리스크 자문, 테크 혁신
   - **🟡 한영 EY (EY Han Young)**: EY-파르테논 전략자문, EY.ai 솔루션, ESG 기후공시
   - **🟢 안진 Deloitte (Deloitte Anjin)**: 글로벌 네트워크 세미나, 공급망·테크 자문
   - 각 회계법인 고유 브랜드 컬러 및 설립연도, 대표자 메타 정보 제공

2. **📰 다양한 언론사 뉴스 수집 및 언론사별 필터링**
   - 한국경제, 매일경제, 조선비즈, 서울경제, 동아일보, 머니투데이, 파이낸셜뉴스, 디지털타임스, 전자신문 등 주요 언론사 뉴스 연동
   - 언론사 드롭다운을 통해 특정 언론사의 보도만 선택하여 확인 가능

3. **🏷️ 주제 분야(카테고리) 및 키워드 검색**
   - **주제 분야 필터**: 감사/회계, 세무/택스, M&A/자문, 컨설팅/AI, ESG/사회공헌, 인사/채용
   - **실시간 검색**: 제목, 요약, 해시태그 기반 빠른 디바운스 검색 지원
   - **해시태그 클릭 검색**: 기사 카드에 표시된 태그(`#생성형AI`, `#M&A`, `#지배구조` 등)를 클릭하면 즉시 해당 주제로 검색

4. **🔄 실시간 뉴스 수집 & 새로고침 (`/api/refresh`)**
   - 상단 '실시간 수집' 버튼 클릭 시 Google News RSS 등을 통해 최신 기사를 수집하여 로컬 캐시에 즉각 병합

5. **📊 인사이트 통계 대시보드 (Chart.js)**
   - 회계법인별 기사 점유율 도넛 차트
   - 업무 분야별 기사 수 바 차트
   - 주요 보도 언론사 순위 차트
   - 핫토픽 키워드 클라우드

6. **⭐ 나만의 스크랩(북마크) 및 CSV 내보내기**
   - 관심 있는 기사를 브라우저 스크랩(북마크)에 저장하고 모아보기 지원
   - 현재 조회 중인 기사 목록을 엑셀 호환 CSV 파일로 원클릭 다운로드

7. **🌓 다크 모드 / 라이트 모드 지원 및 반응형 UI**
   - 모바일, 태블릿, 데스크톱 화면에 최적화된 반응형 카드 레이아웃

---

## 🚀 빠른 시작 가이드

### 1. 실행 환경 요구사항
- Python 3.9 이상 (Anaconda 또는 일반 Python)
- 필수 라이브러리: `Flask`, `requests`, `beautifulsoup4`

### 2. 패키지 설치 (필요시)
```bash
pip install -r requirements.txt
```

### 3. 서버 실행
```bash
cd /Users/j.kyu_0621/.gemini/antigravity/scratch/big4-news-hub
python app.py
```

### 4. 웹 브라우저 접속
웹 브라우저를 열고 아래 주소로 접속합니다:
👉 **`http://127.0.0.1:5000`**

---

## 📁 프로젝트 구조

```
big4-news-hub/
├── app.py                  # Flask 백엔드 서버 및 REST API
├── crawler.py              # RSS 뉴스 수집기, 법인/카테고리 분류기
├── sample_data.py          # 빅4 회계법인 시드 데이터 및 법인 메타데이터
├── requirements.txt        # Python 의존성 목록
├── vercel.json             # Vercel 라우팅 설정
├── api/
│   └── index.py            # Vercel 서버리스 진입점
├── data/
│   └── news_cache.json     # 수집된 뉴스 로컬 캐시 파일
├── public/
│   └── static/             # ★ 정적 파일은 이 폴더 한 곳에서만 수정 (로컬 Flask와 Vercel 공용)
│       ├── css/style.css
│       └── js/app.js       # SPA 프론트엔드 로직 (필터링, 차트, 북마크)
└── templates/
    └── index.html          # 메인 웹 페이지 대시보드 템플릿
```

> **주의**: 예전에는 `static/`과 `public/static/`이 따로 있어서 한쪽만 고치면 로컬과 배포 화면이 달라졌습니다. 이제 `public/static/` 하나만 사용합니다.

---

## 📡 RESTful API 명세

| Method | Endpoint | 설명 |
|---|---|---|
| `GET` | `/` | 메인 대시보드 웹페이지 |
| `GET` | `/api/news` | 기사 목록 조회 (파라미터: `firm`, `source`, `category`, `q`, `sort`, `page`, `limit`, `ids`) — `ids`는 쉼표로 구분한 기사 ID(스크랩 조회용) |
| `GET` | `/api/firms` | 빅4 회계법인 메타데이터 및 기사 통계 |
| `POST`| `/api/refresh` | 실시간 뉴스 수집 및 캐시 갱신 |
| `GET` | `/api/stats` | 차트 시각화용 통계 데이터 반환 |
| `GET` | `/api/export` | 현재 화면과 같은 조건의 CSV 다운로드 (`/api/news`와 동일한 필터 파라미터 지원) |

> **배포(Vercel) 참고**: 화면은 API를 `/api/index?__route=news&...` 형태로 호출합니다(`app.py`의 `ApiRouteMiddleware`가 `/api/news`로 되돌려 줌).
> Vercel이 rewrite된 하위 경로(`/api/news`)를 함수에 전달하지 않아 API가 HTML로 응답되던 문제를 피하기 위한 구조입니다. 직접 `/api/news`로 호출하는 것도 로컬에서는 그대로 동작합니다.

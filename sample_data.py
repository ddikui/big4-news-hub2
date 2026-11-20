# -*- coding: utf-8 -*-
"""
Big 4 Accounting Firms News Hub - Sample & Seed News Dataset
삼일 PwC, 삼정 KPMG, 한영 EY, 안진 Deloitte의 주요 뉴스 데이터
"""

SAMPLE_NEWS = [
    # 삼일 PwC
    {
        "id": "samil-001",
        "title": "삼일PwC, 생성형 AI 기반 감사 플랫폼 'PwC 넥스트' 전면 도입",
        "firm": "samil",
        "firm_name": "삼일 PwC",
        "source": "한국경제",
        "author": "김진수 기자",
        "pub_date": "2026-11-19T08:30:00+09:00",
        "summary": "삼일PwC가 2026 사업연도부터 모든 상장사 감사 업무에 차세대 생성형 AI 감사 솔루션 'PwC 넥스트(Next)'를 전격 도입한다고 19일 밝혔다. 복잡한 거래 내역 분석 시간을 60% 단축하고 이상 징후 탐지율을 크게 끌어올렸다.",
        "url": "https://www.hankyung.com",
        "category": "감사/회계",
        "tags": ["생성형AI", "디지털감사", "PwC넥스트", "회계감사"]
    },
    {
        "id": "samil-002",
        "title": "삼일PwC '2026년 글로벌 M&A 시장 전망' 보고서 발간... 크로스보더 딜 회복세",
        "firm": "samil",
        "firm_name": "삼일 PwC",
        "source": "매일경제",
        "author": "박형민 기자",
        "pub_date": "2026-11-18T14:15:00+09:00",
        "summary": "삼일PwC 경영연구원은 올해 하반기부터 국내외 대형 인수합병(M&A) 시장이 기술기업과 친환경 인프라를 중심으로 뚜렷한 회복 국면에 진입했다고 분석했다.",
        "url": "https://www.mk.co.kr",
        "category": "M&A/자문",
        "tags": ["M&A", "딜자문", "시장전망", "크로스보더"]
    },
    {
        "id": "samil-003",
        "title": "삼일PwC, '글로벌 최저한세(Pillar 2)' 대응 기업 설명회 성료",
        "firm": "samil",
        "firm_name": "삼일 PwC",
        "source": "조선비즈",
        "author": "이민우 기자",
        "pub_date": "2026-11-17T11:00:00+09:00",
        "summary": "삼일PwC 세무자문본부는 여의도 본사에서 국내 100대 다국적 대기업 조세 담당자를 대상으로 2026년 확대 시행되는 글로벌 최저한세 세무 리스크 점검 및 세무 자동화 전략 세미나를 개최했다.",
        "url": "https://biz.chosun.com",
        "category": "세무/택스",
        "tags": ["글로벌최저한세", "Pillar2", "국제조세", "세무전략"]
    },
    {
        "id": "samil-004",
        "title": "삼일PwC, 대학생 대상 '제8회 회계 투명성 공모전' 개최",
        "firm": "samil",
        "firm_name": "삼일 PwC",
        "source": "연합뉴스",
        "author": "성혜미 기자",
        "pub_date": "2026-11-15T09:40:00+09:00",
        "summary": "삼일회계법인은 미래 세대의 회계 투명성에 대한 관심 제고와 인재 발굴을 위해 전국 대학생 및 대학원생을 대상으로 제8회 공모전을 개최한다고 발표했다.",
        "url": "https://www.yna.co.kr",
        "category": "ESG/사회공헌",
        "tags": ["회계투명성", "공모전", "인재육성", "장학사업"]
    },
    {
        "id": "samil-005",
        "title": "삼일PwC 지배구조선진화센터 '2026 상장사 사외이사 평가 트렌드' 발표",
        "firm": "samil",
        "firm_name": "삼일 PwC",
        "source": "머니투데이",
        "author": "오정은 기자",
        "pub_date": "2026-11-14T16:20:00+09:00",
        "summary": "삼일PwC 지배구조선진화센터는 이사회 역량구성표(BSM) 도입 기업이 2년 전 대비 3배 이상 증가하며 이사회 전문성과 다양성이 크게 강화되고 있다고 분석했다.",
        "url": "https://news.mt.co.kr",
        "category": "컨설팅/거버넌스",
        "tags": ["지배구조", "사외이사", "BSM", "이사회선진화"]
    },

    # 삼정 KPMG
    {
        "id": "samjong-001",
        "title": "삼정KPMG '피지컬 AI와 휴머노이드 로봇 산업의 미래' 스페셜 리포트 발간",
        "firm": "samjong",
        "firm_name": "삼정 KPMG",
        "source": "파이낸셜뉴스",
        "author": "강구귀 기자",
        "pub_date": "2026-11-19T09:10:00+09:00",
        "summary": "삼정KPMG는 글로벌 로봇 공학 및 인공지능 융합 시장이 2030년까지 연평균 42% 성장할 것으로 전망하며, 국내 제조업체들의 피지컬 AI 전략 수립이 시급하다고 제언했다.",
        "url": "https://www.fnnews.com",
        "category": "컨설팅/거버넌스",
        "tags": ["피지컬AI", "로봇공학", "산업전망", "제조혁신"]
    },
    {
        "id": "samjong-002",
        "title": "삼정KPMG, 국내 금융지주 대상 '바젤 III 최종 규제 리스크 관리' 컨설팅 수주",
        "firm": "samjong",
        "firm_name": "삼정 KPMG",
        "source": "서울경제",
        "author": "김현상 기자",
        "pub_date": "2026-11-18T10:45:00+09:00",
        "summary": "삼정KPMG 금융자문본부가 국내 주요 시중은행 및 금융지주의 바젤3 리스크 산출 시스템 고도화 및 규제 대응 종합 컨설팅 프로젝트를 잇따라 수주했다고 18일 밝혔다.",
        "url": "https://www.sedaily.com",
        "category": "컨설팅/거버넌스",
        "tags": ["금융컨설팅", "바젤III", "리스크관리", "금융지주"]
    },
    {
        "id": "samjong-003",
        "title": "삼정KPMG, 연말 정기 파트너 인사 단행... 'AI·바이오 전문 인력 대거 발탁'",
        "firm": "samjong",
        "firm_name": "삼정 KPMG",
        "source": "이데일리",
        "author": "김응태 기자",
        "pub_date": "2026-11-16T17:00:00+09:00",
        "summary": "삼정KPMG가 신임 파트너 28명을 선임했다. 이번 인사는 신기술 감사, 헬스케어·바이오 및 글로벌 공급망 재편 대응 역량을 갖춘 40대 초중반 젊은 전문가들이 대거 전진 배치된 것이 특징이다.",
        "url": "https://www.edaily.co.kr",
        "category": "인사/동정",
        "tags": ["인사", "신임파트너", "AI인재", "전문가발탁"]
    },
    {
        "id": "samjong-004",
        "title": "삼정KPMG '공공기관 경영평가 및 회계투명성 강화 워크숍' 성료",
        "firm": "samjong",
        "firm_name": "삼정 KPMG",
        "source": "헤럴드경제",
        "author": "유은수 기자",
        "pub_date": "2026-11-15T15:30:00+09:00",
        "summary": "삼정KPMG 공공부문 감사본부는 50여 개 공기업 및 준정부기관 기획예산 담당 임직원을 대상으로 직무 중심 보수체계 개편과 내부회계관리제도 평가 전략 워크숍을 진행했다.",
        "url": "https://biz.heraldcorp.com",
        "category": "감사/회계",
        "tags": ["공공기관", "경영평가", "내부회계", "투명성"]
    },
    {
        "id": "samjong-005",
        "title": "삼정KPMG, 스타트업 스케일업 지원 프로그램 'KPMG 스타트업 챌린지 2026' 개시",
        "firm": "samjong",
        "firm_name": "삼정 KPMG",
        "source": "전자신문",
        "author": "조정형 기자",
        "pub_date": "2026-11-13T13:20:00+09:00",
        "summary": "삼정KPMG가 딥테크 및 핀테크 분야 유망 초기 기업을 선발해 해외 진출 및 벤처캐피털 투자 연계를 돕는 오픈 이노베이션 챌린지 참가 기업을 모집한다.",
        "url": "https://www.etnews.com",
        "category": "M&A/자문",
        "tags": ["스타트업", "오픈이노베이션", "투자유치", "스케일업"]
    },

    # 한영 EY
    {
        "id": "ey-001",
        "title": "EY한영, AI 혁신 플랫폼 'EY.ai 파생 에이전트' 기업 업무 전면 공개",
        "firm": "ey",
        "firm_name": "한영 EY",
        "source": "디지털타임스",
        "author": "유선희 기자",
        "pub_date": "2026-11-19T10:00:00+09:00",
        "summary": "EY한영이 자체 개발한 기업용 특화 LLM 기반 자율 에이전트 플랫폼 'EY.ai Pulse'를 국내 고객사에 본격 공급한다. 세무, 공급망 최적화, 규제 컴플라이언스 작업을 자동화한다.",
        "url": "https://www.dt.co.kr",
        "category": "컨설팅/거버넌스",
        "tags": ["EY.ai", "인공지능", "에이전트", "업무자동화"]
    },
    {
        "id": "ey-002",
        "title": "EY한영, 2026년 회계연도 상반기 매출 전년비 14% 성장... '전략·자문 부문 견인'",
        "firm": "ey",
        "firm_name": "한영 EY",
        "source": "조선비즈",
        "author": "김효인 기자",
        "pub_date": "2026-11-17T15:10:00+09:00",
        "summary": "EY한영(대표이사 박용근)은 전략·재무자문 부문인 EY-파르테논의 호조와 디지털 전환 컨설팅 수요 증가에 힘입어 2026 회계연도 상반기 두 자릿수 견고한 성장을 달성했다고 밝혔다.",
        "url": "https://biz.chosun.com",
        "category": "경영실적",
        "tags": ["실적발표", "EY-파르테논", "매출성장", "경영성과"]
    },
    {
        "id": "ey-003",
        "title": "EY한영 '국내 주요 기업 기후공시(IFRS S1/S2) 준비 현황 분석' 발표",
        "firm": "ey",
        "firm_name": "한영 EY",
        "source": "한국경제",
        "author": "이한얼 기자",
        "pub_date": "2026-11-16T11:30:00+09:00",
        "summary": "EY한영 CCaSS(기후변화 및 지속가능성 서비스) 팀은 조사 대상 코스피 200 기업 중 68%가 Scope 3 온실가스 배출량 산정에 착수했으나 데이터 신뢰도 확보가 과제라고 지적했다.",
        "url": "https://www.hankyung.com",
        "category": "ESG/사회공헌",
        "tags": ["기후공시", "IFRS", "지속가능성", "Scope3"]
    },
    {
        "id": "ey-004",
        "title": "EY한영 '제19회 EY 최우수 기업가상' 성황리 개최... 혁신 기업인 표창",
        "firm": "ey",
        "firm_name": "한영 EY",
        "source": "매일경제",
        "author": "안병준 기자",
        "pub_date": "2026-11-14T18:40:00+09:00",
        "summary": "비즈니스 오스카상으로 불리는 'EY 최우수 기업가상(EY Entrepreneur Of The Year)' 시상식이 서울 신라호텔에서 열려 대한민국 산업 혁신을 이끈 대표 기업인들이 수상의 영예를 안았다.",
        "url": "https://www.mk.co.kr",
        "category": "인사/동정",
        "tags": ["기업가상", "시상식", "기업혁신", "기업가정신"]
    },
    {
        "id": "ey-005",
        "title": "EY한영, 아시아태평양 조세 분쟁 포럼 개최... '국제세무 동향 점검'",
        "firm": "ey",
        "firm_name": "한영 EY",
        "source": "아시아경제",
        "author": "손선우 기자",
        "pub_date": "2026-11-12T14:00:00+09:00",
        "summary": "EY한영 세무본부는 아태지역 다국적 과세당국의 공격적인 이전가격 조사 강화 트렌드와 국제 조세 분쟁 예방을 위한 상호합의(MAP) 전략을 공유하는 글로벌 포럼을 개최했다.",
        "url": "https://www.asiae.co.kr",
        "category": "세무/택스",
        "tags": ["이전가격", "국제세무", "조세분쟁", "아태포럼"]
    },

    # 안진 Deloitte
    {
        "id": "deloitte-001",
        "title": "딜로이트 안진, '글로벌 반도체 공급망 재편과 투자 전략' 세미나 개최",
        "firm": "deloitte",
        "firm_name": "안진 Deloitte",
        "source": "동아일보",
        "author": "곽도영 기자",
        "pub_date": "2026-11-19T11:20:00+09:00",
        "summary": "딜로이트 안진회계법인과 딜로이트 컨설팅은 소공동 롯데호텔에서 미국 반도체 보조금 및 통상 규제 변화에 따른 국내 소부장 기업들의 현지 진출 및 세제 혜택 극대화 세미나를 열었다.",
        "url": "https://www.donga.com",
        "category": "M&A/자문",
        "tags": ["반도체", "공급망", "글로벌투자", "통상규제"]
    },
    {
        "id": "deloitte-002",
        "title": "딜로이트 안진 '2026 국내 소비재 트렌드 보고서'... 가성비와 프리미엄 양극화 심화",
        "firm": "deloitte",
        "firm_name": "안진 Deloitte",
        "source": "머니투데이",
        "author": "이재윤 기자",
        "pub_date": "2026-11-18T09:15:00+09:00",
        "summary": "딜로이트 안진 컨슈머 산업팀은 한국 소비 시장이 '극단적 효율 소비'와 '취향 기반 럭셔리 소비'로 양극화되고 있으며, 리테일 기업들의 초개인화 AI 마케팅 도입이 생존의 열쇠라고 밝혔다.",
        "url": "https://news.mt.co.kr",
        "category": "컨설팅/거버넌스",
        "tags": ["소비트렌드", "리테일", "컨슈머", "초개인화"]
    },
    {
        "id": "deloitte-003",
        "title": "딜로이트 안진, 한국거래소와 '중소·벤처 상장기업 내부회계 교육' 협력 협약",
        "firm": "deloitte",
        "firm_name": "안진 Deloitte",
        "source": "연합인포맥스",
        "author": "송하린 기자",
        "pub_date": "2026-11-16T14:40:00+09:00",
        "summary": "딜로이트 안진회계법인은 코스닥·코넥스 상장 기업의 감사 리스크 축소와 내부통제 시스템 정착을 지원하기 위해 한국거래소와 공동 아카데미 프로그램을 개설한다고 발표했다.",
        "url": "https://news.einfomax.co.kr",
        "category": "감사/회계",
        "tags": ["한국거래소", "내부회계관리", "코스닥", "상장지원"]
    },
    {
        "id": "deloitte-004",
        "title": "딜로이트 안진, '글로벌 세무 테크(Tax Tech) 혁신 센터' 서울 거점 신설",
        "firm": "deloitte",
        "firm_name": "안진 Deloitte",
        "source": "서울경제",
        "author": "서민우 기자",
        "pub_date": "2026-11-15T10:10:00+09:00",
        "summary": "딜로이트 안진 세무자문본부는 복잡해지는 다국적 세법 규제 대응을 위해 RPA 및 생성형 AI 기반 세무 자동화 솔루션을 연구·개발하는 '텍스 테크 이노베이션 랩'을 출범시켰다.",
        "url": "https://www.sedaily.com",
        "category": "세무/택스",
        "tags": ["택스테크", "세무자동화", "RPA", "이노베이션"]
    },
    {
        "id": "deloitte-005",
        "title": "딜로이트 안진, '사회복지공동모금회 1억원 기부' 취약계층 회계 교육 지원",
        "firm": "deloitte",
        "firm_name": "안진 Deloitte",
        "source": "이데일리",
        "author": "정다슬 기자",
        "pub_date": "2026-11-13T16:50:00+09:00",
        "summary": "딜로이트 안진회계법인은 임직원 매칭 그랜트로 조성된 기금 1억 원을 기탁하고, 청년 자립준비청년들을 위한 금융기초 및 회계 멘토링 프로그램을 본격 전개한다.",
        "url": "https://www.edaily.co.kr",
        "category": "ESG/사회공헌",
        "tags": ["사회공헌", "기부", "자립준비청년", "금융교육"]
    },

    # 전체 빅4 통합 이슈 및 업계 전반
    {
        "id": "big4-all-001",
        "title": "빅4 회계법인, 2026년 정기 감사 수임전 치열... 금융·방산 업종 대어 이동 주목",
        "firm": "all",
        "firm_name": "전체 빅4",
        "source": "한국경제",
        "author": "조진형 기자",
        "pub_date": "2026-11-19T07:30:00+09:00",
        "summary": "주기적 지정제 2주기를 맞아 삼일, 삼정, 한영, 안진 등 빅4 회계법인이 주요 금융지주와 K-방산 대표기업 감사인 교체 지정을 앞두고 총력전을 펼치고 있다. 품질 관리와 디지털 감사 역량이 승부처가 될 전망이다.",
        "url": "https://www.hankyung.com",
        "category": "감사/회계",
        "tags": ["주기적지정제", "감사수임전", "금융지주", "품질관리"]
    },
    {
        "id": "big4-all-002",
        "title": "금융당국, 빅4 회계법인 CEO 간담회 개최... '품질 우선주의와 가상자산 감사 기준 점검'",
        "firm": "all",
        "firm_name": "전체 빅4",
        "source": "매일경제",
        "author": "최근도 기자",
        "pub_date": "2026-11-18T16:00:00+09:00",
        "summary": "금융위원회와 금융감독원은 18일 삼일PwC, 삼정KPMG, EY한영, 딜로이트안진 대표들과 간담회를 갖고 2026년 결산 감사 대비 가상자산 회계처리 통일성 및 AI 감사 툴 신뢰성 점검 가이드라인을 논의했다.",
        "url": "https://www.mk.co.kr",
        "category": "감사/회계",
        "tags": ["금융당국", "CEO간담회", "가상자산", "감사품질"]
    },
    {
        "id": "big4-all-003",
        "title": "빅4 회계법인 신입 공인회계사(CPA) 채용 1,300명 돌파... 역대 최대 규모",
        "firm": "all",
        "firm_name": "전체 빅4",
        "source": "조선일보",
        "author": "임경업 기자",
        "pub_date": "2026-11-17T09:00:00+09:00",
        "summary": "2026년도 제61회 공인회계사 시험 합격자들을 대상으로 한 빅4 회계법인의 채용 경쟁이 마무리됐다. IT·디지털 역량을 갖춘 복수전공자 선호도가 높았으며 처우 개선이 두드러졌다.",
        "url": "https://www.chosun.com",
        "category": "인사/동정",
        "tags": ["CPA채용", "공인회계사", "인재영입", "신입회계사"]
    },
    {
        "id": "big4-all-004",
        "title": "회계업계 'AI 에이전트 전환' 원년... 빅4 일제히 자체 업무용 AI 배포",
        "firm": "all",
        "firm_name": "전체 빅4",
        "source": "블로터",
        "author": "채명석 기자",
        "pub_date": "2026-11-15T11:45:00+09:00",
        "summary": "삼일의 PwC Next, 삼정의 KPMG Clara AI, 한영의 EY.ai, 딜로이트의 Omnia AI 등 빅4가 사내 전산망에 독자 AI 에이전트를 구축하며 단순 작업에서 전략 자문 중심으로 인력 재배치에 돌입했다.",
        "url": "https://www.bloter.net",
        "category": "컨설팅/거버넌스",
        "tags": ["AI에이전트", "디지털전환", "Clara", "Omnia"]
    },
    {
        "id": "big4-all-005",
        "title": "2026 회계연도 결산 앞두고 '법인세 세무조사 리스크 사전 점검' 빅4 세무자문 문의 급증",
        "firm": "all",
        "firm_name": "전체 빅4",
        "source": "조세일보",
        "author": "류성원 기자",
        "pub_date": "2026-11-14T14:10:00+09:00",
        "summary": "국세청의 정밀 데이터 분석 기반 비정기 세무조사 비율이 높아짐에 따라 주요 대기업과 중견기업들의 빅4 사전 조세 진단 컨설팅 수요가 연말을 앞두고 전년 대비 35% 급증했다.",
        "url": "https://www.joseilbo.com",
        "category": "세무/택스",
        "tags": ["국세청", "세무조사", "세무자문", "리스크관리"]
    },

    # 추가 기사들 (삼일 PwC 추가)
    {
        "id": "samil-006",
        "title": "삼일PwC 유니콘지원센터, 2026 유망 예비 유니콘 20개사 선정 및 멘토링 개시",
        "firm": "samil",
        "firm_name": "삼일 PwC",
        "source": "전자신문",
        "author": "김명희 기자",
        "pub_date": "2026-11-11T15:20:00+09:00",
        "summary": "삼일PwC는 성장 잠재력이 높은 테크 및 바이오 스타트업 20개 사를 선발해 투자 유치 실사 및 내부회계 관리제도 조기 셋업을 밀착 지원한다고 밝혔다.",
        "url": "https://www.etnews.com",
        "category": "M&A/자문",
        "tags": ["유니콘", "스타트업지원", "벤처투자", "멘토링"]
    },
    {
        "id": "samil-007",
        "title": "삼일PwC, '디지털 헬스케어 M&A 시장의 구조적 변화' 인덱스 발표",
        "firm": "samil",
        "firm_name": "삼일 PwC",
        "source": "비즈니스워치",
        "author": "박수연 기자",
        "pub_date": "2026-11-09T10:15:00+09:00",
        "summary": "전통 제약사와 글로벌 빅테크 간 디지털 치료제 및 의료 AI 플랫폼 인수 합병이 아시아 시장에서 가속화되고 있다는 삼일PwC의 분석 보고서가 발간됐다.",
        "url": "https://biz.heraldcorp.com",
        "category": "M&A/자문",
        "tags": ["디지털헬스케어", "의료AI", "제약바이오", "M&A"]
    },

    # 추가 기사들 (삼정 KPMG 추가)
    {
        "id": "samjong-006",
        "title": "삼정KPMG, 국내 방위산업 기업 대상 글로벌 방산 수출 절충교역 자문 확대",
        "firm": "samjong",
        "firm_name": "삼정 KPMG",
        "source": "파이낸셜뉴스",
        "author": "김경민 기자",
        "pub_date": "2026-11-10T14:40:00+09:00",
        "summary": "폴란드, 루마니아 등 동유럽 및 중동 수주가 확대된 K-방산 기업들을 위해 삼정KPMG 방산 전문팀이 현지 합작법인 설립 및 세무 절충교역 컨설팅을 전담 지원한다.",
        "url": "https://www.fnnews.com",
        "category": "M&A/자문",
        "tags": ["K방산", "절충교역", "방산수출", "글로벌자문"]
    },
    {
        "id": "samjong-007",
        "title": "삼정KPMG 경제연구원 '2027 세계 무역 질서 시나리오와 한국 기업의 대응'",
        "firm": "samjong",
        "firm_name": "삼정 KPMG",
        "source": "한국경제",
        "author": "이슬기 기자",
        "pub_date": "2026-11-08T08:50:00+09:00",
        "summary": "미국과 EU의 탄소국경조정제도(CBAM)와 글로벌 공급망 실사법 본격 적용에 따른 대미·대유럽 수출 기업의 원가 상승과 공급망 리스크 대응 해법을 제시했다.",
        "url": "https://www.hankyung.com",
        "category": "컨설팅/거버넌스",
        "tags": ["CBAM", "공급망실사", "무역규제", "경제전망"]
    },

    # 추가 기사들 (한영 EY 추가)
    {
        "id": "ey-006",
        "title": "EY한영, 아시아 최대 클라우드 보안 컴플라이언스(SOC2) 인증 자문 강화",
        "firm": "ey",
        "firm_name": "한영 EY",
        "source": "전자신문",
        "author": "이원식 기자",
        "pub_date": "2026-11-11T13:30:00+09:00",
        "summary": "국내 SaaS 기업들의 북미 시장 진출 필수 요건인 SOC 2, ISO 27001 등 글로벌 보안 인증 자문에서 EY한영 테크 포렌식 및 정보보안 자문팀이 시장 점유율 1위를 굳혔다.",
        "url": "https://www.etnews.com",
        "category": "감사/회계",
        "tags": ["클라우드보안", "SOC2", "SaaS", "정보보안"]
    },
    {
        "id": "ey-007",
        "title": "EY한영, 임직원 웰빙 주간 'Mind Care Festa' 개최... 워라밸 혁신 지속",
        "firm": "ey",
        "firm_name": "한영 EY",
        "source": "매일경제",
        "author": "강인선 기자",
        "pub_date": "2026-11-07T16:10:00+09:00",
        "summary": "회계감사 성수기를 앞두고 임직원들의 심리 건강과 체력 증진을 돕는 심리상담 멘토링, 명상 세션 및 가족 초청 프로그램을 마련해 건강한 조직문화 조성에 나섰다.",
        "url": "https://www.mk.co.kr",
        "category": "ESG/사회공헌",
        "tags": ["조직문화", "마인드케어", "임직원복지", "워라밸"]
    },

    # 추가 기사들 (안진 Deloitte 추가)
    {
        "id": "deloitte-006",
        "title": "딜로이트 안진, '우주항공 및 위성 통신 산업 비즈니스 기회' 세미나 개최",
        "firm": "deloitte",
        "firm_name": "안진 Deloitte",
        "source": "조선비즈",
        "author": "박지환 기자",
        "pub_date": "2026-11-11T09:40:00+09:00",
        "summary": "우주항공청 개청 이후 본격화된 민간 우주개발(뉴 스페이스) 시대를 맞아 국내 통신 및 모빌리티 기업의 신사업 전략 수립을 돕는 전략 세미나를 성공적으로 마무리했다.",
        "url": "https://biz.chosun.com",
        "category": "컨설팅/거버넌스",
        "tags": ["우주항공", "뉴스페이스", "위성통신", "신성장동력"]
    },
    {
        "id": "deloitte-007",
        "title": "딜로이트 글로벌, 2026 테크 트렌드 발표... '신뢰할 수 있는 에이전틱 AI와 양자 암호'",
        "firm": "deloitte",
        "firm_name": "안진 Deloitte",
        "source": "디지털타임스",
        "author": "박채린 기자",
        "pub_date": "2026-11-08T11:00:00+09:00",
        "summary": "딜로이트 글로벌 테크놀로지 연구소가 발표한 2026 기술 트렌드에 따르면, 산업 현장에서 결정을 내리는 에이전틱 AI의 안전성 검증과 양자 컴퓨터 상용화에 대비한 양자 내성 암호 도입이 핵심 화두로 꼽혔다.",
        "url": "https://www.dt.co.kr",
        "category": "컨설팅/거버넌스",
        "tags": ["테크트렌드", "양자암호", "에이전틱AI", "글로벌리포트"]
    }
]

FIRMS_INFO = {
    "all": {
        "id": "all",
        "name": "전체 빅4",
        "name_en": "Big 4 Korea",
        "color": "#1e293b",
        "accent": "#3b82f6",
        "badge_bg": "bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200",
        "description": "대한민국 빅4 회계법인 (삼일 PwC, 삼정 KPMG, 한영 EY, 안진 Deloitte) 전체 최신 뉴스",
        "keywords": ["빅4", "회계법인", "회계업계", "4대 회계법인"]
    },
    "samil": {
        "id": "samil",
        "name": "삼일 PwC",
        "name_en": "Samil PwC",
        "brand_color": "#D04A02",
        "color": "#e05307",
        "accent": "#f97316",
        "badge_bg": "bg-orange-100 dark:bg-orange-950/60 text-orange-700 dark:text-orange-300 border-orange-200 dark:border-orange-800",
        "description": "국내 최대 회계법인 및 PwC 글로벌 네트워크 한국 회원사",
        "ceo": "윤훈수 대표",
        "founded": "1971년",
        "keywords": ["삼일", "삼일회계법인", "삼일 PwC", "삼일PwC", "PwC컨설팅", "PwC"]
    },
    "samjong": {
        "id": "samjong",
        "name": "삼정 KPMG",
        "name_en": "Samjong KPMG",
        "brand_color": "#00338D",
        "color": "#0051C7",
        "accent": "#2563eb",
        "badge_bg": "bg-blue-100 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-800",
        "description": "감사·세무·재무자문 종합 컨설팅 및 KPMG 글로벌 한국 회원사",
        "ceo": "김교태 대표",
        "founded": "1969년",
        "keywords": ["삼정", "삼정KPMG", "삼정회계법인", "삼정 kpmg", "KPMG"]
    },
    "ey": {
        "id": "ey",
        "name": "한영 EY",
        "name_en": "EY Han Young",
        "brand_color": "#FFE600",
        "color": "#E5A900",
        "accent": "#eab308",
        "badge_bg": "bg-yellow-100 dark:bg-yellow-950/60 text-yellow-800 dark:text-yellow-300 border-yellow-200 dark:border-yellow-800",
        "description": "전략·재무자문(EY-파르테논) 및 Ernst & Young 글로벌 한국 회원사",
        "ceo": "박용근 대표",
        "founded": "1989년",
        "keywords": ["한영", "한영회계법인", "EY한영", "EY 한영", "EY-파르테논", "Ernst & Young"]
    },
    "deloitte": {
        "id": "deloitte",
        "name": "안진 Deloitte",
        "name_en": "Deloitte Anjin",
        "brand_color": "#86BC25",
        "color": "#007624",
        "accent": "#22c55e",
        "badge_bg": "bg-emerald-100 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800",
        "description": "글로벌 딜로이트 네트워크의 전문성과 강력한 리스크 자문 역량 보유",
        "ceo": "홍종성 대표",
        "founded": "1987년",
        "keywords": ["안진", "안진회계법인", "딜로이트", "딜로이트 안진", "딜로이트안진", "Deloitte"]
    }
}

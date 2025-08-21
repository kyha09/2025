import streamlit as st
from urllib.parse import quote

st.set_page_config(page_title="MBTI 기반 진로교육 추천", page_icon="🎯", layout="wide")

# -----------------------------
# 데이터 정의
# -----------------------------
MBTI_TYPES = [
    "ISTJ","ISFJ","INFJ","INTJ",
    "ISTP","ISFP","INFP","INTP",
    "ESTP","ESFP","ENFP","ENTP",
    "ESTJ","ESFJ","ENFJ","ENTJ",
]

# 공통 포털 (모든 유형에 기본 제공)
COMMON_PORTALS = [
    {"name": "커리어넷(진로·직업정보)", "url": "https://www.career.go.kr/", "desc": "국가 진로정보 포털 – 직업백과, 적성검사, 학과·진로 지도 자료."},
    {"name": "워크넷(고용정보)", "url": "https://www.work.go.kr/", "desc": "채용·직업정보, 진로탐색, 직무 분석 자료."},
    {"name": "NCS 국가직무능력표준", "url": "https://www.ncs.go.kr/", "desc": "직무별 필요 역량과 교육·평가 기준 확인."},
    {"name": "K-MOOC", "url": "https://www.kmooc.kr/", "desc": "대학 공개강좌 – 전공 맛보기와 기초 역량 강화."},
]

# 유형별 추천 도메인 및 사이트
MBTI_RECS = {
    "ISTJ": {
        "traits": ["체계적", "책임감", "신뢰성"],
        "careers": ["행정·공공안전", "회계·감사", "데이터 관리"],
        "sites": [
            {"name":"정부24/국가자격", "url":"https://www.q-net.or.kr/", "desc":"국가자격 안내 – 공공·회계 관련 자격 확인."},
            {"name":"통계청 KOSIS", "url":"https://kosis.kr/", "desc":"통계 리터러시와 데이터 기초 학습."},
        ],
    },
    "ISFJ": {
        "traits": ["성실", "배려", "헌신"],
        "careers": ["보건·간호 보조", "사회복지", "교육 지원"],
        "sites": [
            {"name":"보건의료인국가시험원", "url":"https://www.kuksiwon.or.kr/", "desc":"보건계 국가시험 및 직무 이해."},
            {"name":"사회복지사협회", "url":"https://www.welfare.net/", "desc":"사회복지 관련 진로와 교육."},
        ],
    },
    "INFJ": {
        "traits": ["통찰", "가치지향", "조직화"],
        "careers": ["상담·심리", "기획·정책", "비영리·CSR"],
        "sites": [
            {"name":"한국상담학회", "url":"https://www.counselors.or.kr/", "desc":"상담·심리 학습 자료와 진로 안내."},
            {"name":"K-MOOC 심리학", "url":"https://www.kmooc.kr/search?search=심리학", "desc":"기초 심리학 강좌로 이론 기반 다지기."},
        ],
    },
    "INTJ": {
        "traits": ["전략", "분석", "독립"],
        "careers": ["데이터·AI", "R&D 기획", "컨설팅"],
        "sites": [
            {"name":"AI HUB", "url":"https://aihub.or.kr/", "desc":"AI 데이터·튜토리얼 자료."},
            {"name":"K-MOOC 데이터사이언스", "url":"https://www.kmooc.kr/search?search=데이터", "desc":"데이터·통계·머신러닝 기초."},
        ],
    },
    "ISTP": {
        "traits": ["문제해결", "실용", "분석"],
        "careers": ["엔지니어링", "품질관리", "디지털 포렌식"],
        "sites": [
            {"name":"디지털포렌식연구센터", "url":"https://www.digitalforensic.or.kr/", "desc":"포렌식 개요와 교육 소식."},
            {"name":"생활코딩", "url":"https://opentutorials.org/course/1", "desc":"실용 코딩 입문."},
        ],
    },
    "ISFP": {
        "traits": ["온화", "미감", "실천"],
        "careers": ["콘텐츠·디자인", "유아·교육 보조", "사회서비스"],
        "sites": [
            {"name":"K-MOOC 디자인", "url":"https://www.kmooc.kr/search?search=디자인", "desc":"그래픽·UX 등 디자인 기초."},
            {"name":"아동학·유아교육 강좌", "url":"https://www.kmooc.kr/search?search=아동", "desc":"아동발달·놀이활동 이해."},
        ],
    },
    "INFP": {
        "traits": ["이상", "공감", "창의"],
        "careers": ["출판·콘텐츠 기획", "교육·상담", "비영리"],
        "sites": [
            {"name":"국립중앙도서관 출판·직업정보", "url":"https://www.nl.go.kr/", "desc":"출판·저작 관련 동향 파악."},
            {"name":"K-MOOC 글쓰기", "url":"https://www.kmooc.kr/search?search=글쓰기", "desc":"콘텐츠 기획·문장력 기초."},
        ],
    },
    "INTP": {
        "traits": ["이론", "탐구", "논리"],
        "careers": ["연구·개발", "데이터·알고리즘", "교육·학술"] ,
        "sites": [
            {"name":"K-MOOC 알고리즘", "url":"https://www.kmooc.kr/search?search=알고리즘", "desc":"컴퓨터 과학·수학적 사고."},
            {"name":"edX(영문)", "url":"https://www.edx.org/", "desc":"대학 강좌 – CS·수학 심화."},
        ],
    },
    "ESTP": {
        "traits": ["실전", "대담", "적응"],
        "careers": ["세일즈·마케팅", "스포츠·이벤트", "보안·경호"],
        "sites": [
            {"name":"K-MOOC 마케팅", "url":"https://www.kmooc.kr/search?search=마케팅", "desc":"브랜딩·디지털 마케팅 기초."},
            {"name":"대한체육회 스포츠교육", "url":"https://www.sports.or.kr/", "desc":"스포츠 분야 진로 정보."},
        ],
    },
    "ESFP": {
        "traits": ["사교", "감각", "에너지"],
        "careers": ["공연·방송", "관광·서비스", "유아·돌봄"],
        "sites": [
            {"name":"관광인(관광교육포털)", "url":"https://www.tourisminn.or.kr/", "desc":"관광·서비스 교육/자격."},
            {"name":"K-MOOC 공연예술", "url":"https://www.kmooc.kr/search?search=공연", "desc":"공연·무대 관련 기초."},
        ],
    },
    "ENFP": {
        "traits": ["아이디어", "커뮤니케이션", "도전"],
        "careers": ["브랜드·콘텐츠", "교육·에듀테크", "사회혁신"],
        "sites": [
            {"name":"비영리허브 디얼스", "url":"https://www.dears.kr/", "desc":"소셜섹터 교육·행사 정보."},
            {"name":"K-MOOC 창업", "url":"https://www.kmooc.kr/search?search=창업", "desc":"스타트업·기획 기초."},
        ],
    },
    "ENTP": {
        "traits": ["발명", "토론", "전략"],
        "careers": ["창업·제품기획", "컨설팅", "테크커뮤니케이션"],
        "sites": [
            {"name":"K-Startup", "url":"https://www.k-startup.go.kr/", "desc":"창업 교육·지원사업 통합 포털."},
            {"name":"K-MOOC 프로젝트관리", "url":"https://www.kmooc.kr/search?search=프로젝트", "desc":"프로젝트·문제해결 역량."},
        ],
    },
    "ESTJ": {
        "traits": ["조직", "실행", "결단"],
        "careers": ["경영관리", "공공행정·치안", "품질·생산관리"],
        "sites": [
            {"name":"경찰청 사이버아카데미", "url":"https://cyber.police.go.kr/", "desc":"치안·법질서 이해(일부 공개자료)."},
            {"name":"K-MOOC 경영", "url":"https://www.kmooc.kr/search?search=경영", "desc":"경영·회계·PM 기초."},
        ],
    },
    "ESFJ": {
        "traits": ["협력", "서비스", "조화"],
        "careers": ["교육·행정", "병원 코디", "고객경험(CX)"],
        "sites": [
            {"name":"K-MOOC 상담·교육", "url":"https://www.kmooc.kr/search?search=교육", "desc":"학습자 지원·상담 기초."},
            {"name":"고객경험 자료(WorkNet)", "url":"https://www.work.go.kr/", "desc":"서비스 직무 동향 파악."},
        ],
    },
    "ENFJ": {
        "traits": ["리더십", "코칭", "공감"],
        "careers": ["인사·조직개발", "교육·강의", "공공정책"],
        "sites": [
            {"name":"HRD-Net", "url":"https://www.hrd.go.kr/", "desc":"직업훈련·HRD 과정 검색."},
            {"name":"K-MOOC 리더십", "url":"https://www.kmooc.kr/search?search=리더십", "desc":"리더십·조직 커뮤니케이션."},
        ],
    },
    "ENTJ": {
        "traits": ["지휘", "계획", "효율"],
        "careers": ["전략·기획", "프로덕트매니지먼트", "금융·컨설팅"],
        "sites": [
            {"name":"핀테크 지원포털", "url":"https://www.fintech.or.kr/", "desc":"금융·데이터 비즈니스 이해."},
            {"name":"K-MOOC 전략·분석", "url":"https://www.kmooc.kr/search?search=전략", "desc":"전략·비즈니스 분석 기초."},
        ],
    },
}

# 부족한 유형(한국어 자료가 겹치더라도) 기본 리소스를 추가로 보강
for t in MBTI_TYPES:
    if t not in MBTI_RECS:
        MBTI_RECS[t] = {
            "traits": ["탐색", "성장", "강점기반"],
            "careers": ["관심분야 탐색", "프로젝트 기반 학습"],
            "sites": [],
        }

# 공통 보완 리소스(유형 특성과 매칭하여 조건부 제안)
EXTRA_BY_DOMAIN = {
    "공공안전": {"name": "대한민국 법제처", "url": "https://www.law.go.kr/", "desc": "법령·제도 이해로 공공영역 직무 파악."},
    "데이터": {"name": "데이콘(DACON)", "url": "https://dacon.io/", "desc": "데이터 실습 대회·튜토리얼."},
    "프로그래밍": {"name": "프로그래머스", "url": "https://programmers.co.kr/", "desc": "코딩 테스트·강의로 실무 감각."},
}

# 간단 매핑(키워드 → 도메인)
KEYWORD_TO_EXTRA = {
    "데이터": ["데이터", "AI", "알고리즘"],
    "공공안전": ["치안", "경찰", "행정", "공공"],
    "프로그래밍": ["개발", "엔지니어", "소프트웨어"],
}

# -----------------------------
# UI
# -----------------------------
st.title("🎯 MBTI 기반 진로교육 추천")
st.caption("참고용 가이드입니다. MBTI는 성격 경향을 설명할 뿐, 진로를 제한하지 않습니다.")

with st.sidebar:
    st.header("설정")
    mbti = st.selectbox("MBTI를 선택하세요", MBTI_TYPES, index=0)
    show_common = st.checkbox("공통 포털도 함께 보기", value=True)

info = MBTI_RECS.get(mbti, {})

left, right = st.columns([1, 1])
with left:
    st.subheader(f"🧭 {mbti} 유형 한눈에 보기")
    st.markdown(
        "**특성**: " + ", ".join(info.get("traits", [])) + "\n\n" +
        "**어울리는 분야(예시)**: " + ", ".join(info.get("careers", []))
    )

with right:
    st.subheader("📝 오늘의 미니 학습계획 만들기")
    goals = st.text_area("오늘의 목표(예: 강좌 1개 수강, 직무 1개 조사)")
    steps = st.text_area("실행 단계(예: 링크 열기 → 노트 정리 → 피드백 받기)")
    plan = f"""# {mbti} 맞춤 미니 학습계획\n\n## 목표\n{goals}\n\n## 실행 단계\n{steps}\n\n— 생성됨: MBTI 기반 진로교육 앱"""
    st.download_button("계획 다운로드(.md)", plan.encode("utf-8"), file_name=f"{mbti}_study_plan.md")

st.divider()
st.subheader("🔗 추천 학습 리소스")

def render_site_card(site: dict):
    st.markdown(
        f"""
        <div style='padding:16px;border:1px solid #eee;border-radius:14px;margin-bottom:12px;'>
            <div style='font-weight:700;font-size:1.05rem;margin-bottom:6px;'>{site.get('name')}</div>
            <div style='margin-bottom:8px;'>{site.get('desc','')}</div>
            <a href='{site.get('url')}' target='_blank'>바로가기</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# 유형별 사이트 출력
for s in info.get("sites", []):
    render_site_card(s)

# 키워드 기반 보완 추천(간단 매칭)
joined = " ".join(info.get("careers", []) + info.get("traits", []))
for domain, keywords in KEYWORD_TO_EXTRA.items():
    if any(k in joined for k in keywords):
        render_site_card(EXTRA_BY_DOMAIN[domain])

# 공통 포털
if show_common:
    st.markdown("### 🌐 공통 포털")
    cols = st.columns(2)
    for i, portal in enumerate(COMMON_PORTALS):
        with cols[i % 2]:
            render_site_card(portal)

# 팁 섹션
st.divider()
st.subheader("💡 사용 팁")
st.markdown(
    """
- MBTI는 **참고용**입니다. 흥미·가치·능력(경험)을 함께 고려하세요.
- 각 링크에서 **직무 설명 → 필요 역량 → 자격/학습 경로**를 체크하고, 오늘의 계획에 옮겨 적으세요.
- 1~2주 단위의 **짧은 프로젝트**(미니 포트폴리오)를 만들어보세요. (예: 데이터 미니분석, 봉사·행정 체험 노트, 교육 보조 활동 일지)
    """
)

st.caption("자료 출처: 공공 포털 및 공개 강좌 사이트. 링크는 학습 편의를 위한 제안입니다.")


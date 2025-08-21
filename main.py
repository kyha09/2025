import streamlit as st
from urllib.parse import quote

st.set_page_config(page_title="🌟 MBTI 기반 진로교육 추천", page_icon="🎯", layout="wide")

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
    {"name": "🌐 커리어넷(진로·직업정보)", "url": "https://www.career.go.kr/", "desc": "📚 국가 진로정보 포털 – 직업백과, 적성검사, 학과·진로 지도 자료."},
    {"name": "💼 워크넷(고용정보)", "url": "https://www.work.go.kr/", "desc": "📊 채용·직업정보, 진로탐색, 직무 분석 자료."},
    {"name": "📑 NCS 국가직무능력표준", "url": "https://www.ncs.go.kr/", "desc": "🛠 직무별 필요 역량과 교육·평가 기준 확인."},
    {"name": "🎓 K-MOOC", "url": "https://www.kmooc.kr/", "desc": "💡 대학 공개강좌 – 전공 맛보기와 기초 역량 강화."},
]

# 유형별 추천 도메인 및 사이트 (대표 예시만 수정)
MBTI_RECS = {
    "ISTJ": {
        "traits": ["🧾 체계적", "🛡 책임감", "🤝 신뢰성"],
        "careers": ["🏛 행정·공공안전", "📊 회계·감사", "💾 데이터 관리"],
        "sites": [
            {"name":"📜 정부24/국가자격", "url":"https://www.q-net.or.kr/", "desc":"🎯 국가자격 안내 – 공공·회계 관련 자격 확인."},
            {"name":"📈 통계청 KOSIS", "url":"https://kosis.kr/", "desc":"📊 통계 리터러시와 데이터 기초 학습."},
        ],
    },
    "ENFP": {
        "traits": ["💡 아이디어", "🗣 커뮤니케이션", "🚀 도전"],
        "careers": ["🎨 브랜드·콘텐츠", "📚 교육·에듀테크", "🌍 사회혁신"],
        "sites": [
            {"name":"🤝 비영리허브 디얼스", "url":"https://www.dears.kr/", "desc":"🌱 소셜섹터 교육·행사 정보."},
            {"name":"🚀 K-MOOC 창업", "url":"https://www.kmooc.kr/search?search=창업", "desc":"💡 스타트업·기획 기초."},
        ],
    },
    # 나머지 MBTI 유형은 이전 정의와 동일, 필요 시 동일한 방식으로 이모지 추가 가능
}

# -----------------------------
# UI
# -----------------------------
st.title("✨🎯 MBTI 기반 진로교육 추천 🎯✨")
st.caption("⚡ 참고용 가이드입니다. MBTI는 성격 경향을 설명할 뿐, 진로를 제한하지 않습니다 ⚡")

with st.sidebar:
    st.header("⚙️ 설정")
    mbti = st.selectbox("🔍 MBTI를 선택하세요", MBTI_TYPES, index=0)
    show_common = st.checkbox("🌐 공통 포털도 함께 보기", value=True)

info = MBTI_RECS.get(mbti, {})

left, right = st.columns([1, 1])
with left:
    st.subheader(f"🧭 {mbti} 유형 한눈에 보기 🧭")
    st.markdown(
        "**✨ 특성**: " + ", ".join(info.get("traits", [])) + "\n\n" +
        "**💼 어울리는 분야(예시)**: " + ", ".join(info.get("careers", []))
    )

with right:
    st.subheader("📝 오늘의 미니 학습계획 만들기 ✨")
    goals = st.text_area("🎯 오늘의 목표 (예: 강좌 1개 수강, 직무 1개 조사)")
    steps = st.text_area("🛠 실행 단계 (예: 링크 열기 → 노트 정리 → 피드백 받기)")
    plan = f"""# {mbti} 맞춤 미니 학습계획 🌟\n\n## 🎯 목표\n{goals}\n\n## 🛠 실행 단계\n{steps}\n\n— 🌈 생성됨: MBTI 기반 진로교육 앱"""
    st.download_button("📥 계획 다운로드(.md)", plan.encode("utf-8"), file_name=f"{mbti}_study_plan.md")

st.divider()
st.subheader("🔗 추천 학습 리소스 ✨")

def render_site_card(site: dict):
    st.markdown(
        f"""
        <div style='padding:16px;border:2px solid #ddd;border-radius:16px;margin-bottom:14px;background-color:#f9f9ff;'>
            <div style='font-weight:700;font-size:1.1rem;margin-bottom:6px;'>🌟 {site.get('name')}</div>
            <div style='margin-bottom:8px;'>✨ {site.get('desc','')}</div>
            <a href='{site.get('url')}' target='_blank'>👉 바로가기</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# 유형별 사이트 출력
for s in info.get("sites", []):
    render_site_card(s)

# 공통 포털
if show_common:
    st.markdown("### 🌐 공통 포털 ✨")
    cols = st.columns(2)
    for i, portal in enumerate(COMMON_PORTALS):
        with cols[i % 2]:
            render_site_card(portal)

# 팁 섹션
st.divider()
st.subheader("💡 사용 꿀팁 ✨")
st.markdown(
    """
- 🌟 MBTI는 **참고용**입니다. 흥미·가치·능력(경험)을 함께 고려하세요.
- 📚 각 링크에서 **직무 설명 → 필요 역량 → 자격/학습 경로**를 체크하세요.
- 🚀 1~2주 단위의 **짧은 프로젝트**(미니 포트폴리오)를 실행해보세요.
  (예: 📊 데이터 미니분석, 🛡 행정·치안 체험, 🎨 디자인 프로젝트)
    """
)

st.caption("📌 자료 출처: 공공 포털 및 공개 강좌 사이트. 링크는 학습 편의를 위한 제안입니다.")

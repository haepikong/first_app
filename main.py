import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI 직업 추천기 🎯", page_icon="🧭", layout="wide")

# ---------------------- 스타일 ----------------------
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            color: #FF6F61;
        }
        .subtitle {
            text-align: center;
            font-size: 24px;
            color: #555;
        }
        .job-card {
            background-color: #FFE5B4;
            padding: 20px;
            margin: 10px;
            border-radius: 15px;
            font-size: 20px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------- 헤더 ----------------------
st.markdown('<div class="title">🌈 MBTI로 알아보는 나의 진로는? 🧑‍🚀</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">자신의 MBTI를 직접 입력하고 추천 직업을 확인하세요! 💼✨</div><br>', unsafe_allow_html=True)

# ---------------------- 사이드바 설명 ----------------------
st.sidebar.title("📌 사용법")
st.sidebar.markdown("1. 자신의 MBTI를 입력하세요 (예: INFP)")
st.sidebar.markdown("2. 버튼을 누르면 추천 직업이 표시됩니다!")

# ---------------------- 입력창 ----------------------
user_input = st.text_input("🔠 MBTI를 입력하세요 (예: INFP)").strip().upper()

# ---------------------- MBTI 직업 데이터 ----------------------
mbti_jobs = {
    'ISTJ': ['👮 경찰', '📊 회계사', '🏛️ 공무원'],
    'ISFJ': ['👩‍⚕️ 간호사', '👩‍🏫 교사', '📚 사서'],
    'INFJ': ['🎨 작가', '🧘 상담가', '🧠 심리학자'],
    'INTJ': ['💻 개발자', '🧪 과학자', '📈 전략가'],
    'ISTP': ['🔧 엔지니어', '🏍️ 기계공', '🧰 기술자'],
    'ISFP': ['🎨 디자이너', '🎶 음악가', '🌿 플로리스트'],
    'INFP': ['📖 시인', '🎭 예술가', '🧘‍♂️ 명상가'],
    'INTP': ['🧠 연구원', '📚 철학자', '💡 발명가'],
    'ESTP': ['🕵️‍♂️ 탐정', '🚗 레이서', '🎤 마케터'],
    'ESFP': ['🎬 배우', '🎤 가수', '🎉 이벤트플래너'],
    'ENFP': ['🌍 사회활동가', '📣 홍보전문가', '🎨 창작가'],
    'ENTP': ['💼 창업가', '🎤 토론가', '🚀 혁신가'],
    'ESTJ': ['🏛️ 관리자', '🧮 기획자', '👨‍💼 경영자'],
    'ESFJ': ['👩‍🏫 교육자', '🛍️ 판매전문가', '🎓 상담교사'],
    'ENFJ': ['🗣️ 리더', '🤝 인사담당자', '📣 홍보팀장'],
    'ENTJ': ['🏢 CEO', '📈 전략컨설턴트', '💰 금융분석가']
}

# ---------------------- 버튼 동작 ----------------------
if st.button("🎯 직업 추천받기"):
    if user_input in mbti_jobs:
        st.markdown(f"### 🧬 `{user_input}` 유형에 어울리는 직업은...")
        st.markdown("---")
        cols = st.columns(3)
        for i, job in enumerate(mbti_jobs[user_input]):
            with cols[i % 3]:
                st.markdown(f'<div class="job-card">{job}</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ 올바른 MBTI 유형을 입력해주세요. (예: ENFP, ISTJ 등 4글자 대문자)")

# ---------------------- 하단 정보 ----------------------
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("✅ 이 웹앱은 성격 유형에 따른 진로 탐색을 돕기 위한 교육용 도구입니다.")
st.markdown("📌 *Made with ❤️ by ChatGPT + Streamlit*")


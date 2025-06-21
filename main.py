import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI 진로 & 음악 추천 🎯🎵", page_icon="🧭", layout="wide")

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
        .music-box {
            background-color: #D0E8FF;
            padding: 15px;
            margin: 20px auto;
            border-radius: 12px;
            text-align: center;
            font-size: 20px;
            color: #003366;
            max-width: 600px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------- 헤더 ----------------------
st.markdown('<div class="title">🌈 MBTI로 알아보는 나의 진로와 음악은? 🎧</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">MBTI를 선택하면 어울리는 직업과 음악을 추천해드릴게요! 💼🎶</div><br>', unsafe_allow_html=True)

# ---------------------- 데이터 ----------------------

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

mbti_music = {
    'ISTJ': '🎶 클래식이나 재즈 — 질서 있는 구조와 집중력 강화',
    'ISFJ': '🎵 어쿠스틱 팝 — 따뜻하고 편안한 감성',
    'INFJ': '🎼 인디/로파이 — 사색적이고 감성적인 분위기',
    'INTJ': '🎧 미니멀 테크노 — 집중력과 고요한 에너지',
    'ISTP': '🎸 록 또는 블루스 — 자유롭고 즉흥적인 감각',
    'ISFP': '🎹 피아노 연주곡 또는 뉴에이지 — 감성적이고 조용한 힐링',
    'INFP': '🎤 감



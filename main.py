import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI 진로 & 음악 추천 🎯🎵", page_icon="🧭", layout="wide")

# ---------------------- CSS 스타일 ----------------------
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
            max-width: 700px;
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
    'INFP': '🎤 감성 팝/발라드 — 감정이입이 깊은 곡',
    'INTP': '🎼 앰비언트 전자음악 — 사고 확장을 돕는 몽환적 사운드',
    'ESTP': '🎷 펑크락 또는 EDM — 에너지 넘치고 활동적인 리듬',
    'ESFP': '🎉 팝/댄스 — 신나는 분위기와 파티 감성',
    'ENFP': '🌟 월드뮤직/퓨전 — 창의적이고 다양한 장르 탐색',
    'ENTP': '🚀 힙합 또는 얼터너티브 — 도전적이고 독창적인 스타일',
    'ESTJ': '🎺 브라스 밴드나 퍼레이드 음악 — 조직적이고 리더십 넘치는 느낌',
    'ESFJ': '🎶 팝 발라드 — 모두가 공감할 수 있는 감성곡',
    'ENFJ': '🎵 뮤지컬 OST — 드라마틱하고 감정 표현 강한 곡',
    'ENTJ': '🎧 시네마틱 사운드트랙 — 파워풀하고 비전 있는 음악'
}

mbti_list = list(mbti_jobs.keys())

# ---------------------- MBTI 선택 ----------------------
selected_mbti = st.selectbox("🔠 MBTI를 선택하세요", mbti_list, index=mbti_list.index("INFP"))

# ---------------------- 직업 추천 ----------------------
st.markdown(f"### 💼 `{selected_mbti}` 유형에게 어울리는 직업")
st.markdown("---")

cols = st.columns(3)
for i, job in enumerate(mbti_jobs[selected_mbti]):
    with cols[i % 3]:
        st.markdown(f'<div class="job-card">{job}</div>', unsafe_allow_html=True)

# ---------------------- 음악 추천 ----------------------
st.markdown("---")
st.markdown(f"<div class='music-box'>🎵 <b>{selected_mbti}</b> 유형에게 어울리는 음악 추천:<br>{mbti_music[selected_mbti]}</div>", unsafe_allow_html=True)

# ---------------------- 하단 정보 ----------------------
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("✅ 이 웹앱은 성격 유형에 따른 진로 및 음악 취향을 탐색할 수 있는 교육용 도구입니다.")
st.markdown("📌 *Made with ❤️ by ChatGPT + Streamlit*")

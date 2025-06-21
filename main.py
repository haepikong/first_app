import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI 진로 & 음악 & 인물 추천기 🎯", page_icon="🌟", layout="wide")

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
        .card {
            background-color: #FFF3E0;
            padding: 20px;
            margin: 10px;
            border-radius: 15px;
            font-size: 20px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------- 헤더 ----------------------
st.markdown('<div class="title">🌈 MBTI로 알아보는 나의 진로, 음악, 그리고 롤모델! 🎧</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">MBTI를 선택하면 나에게 어울리는 직업, 음악, 성공한 인물을 추천해드려요! 💼🎶👑</div><br>', unsafe_allow_html=True)

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
    'ISTJ': '🎶 클래식이나 재즈 — 질서 있고 집중력 강화',
    'ISFJ': '🎵 어쿠스틱 팝 — 따뜻하고 편안한 감성',
    'INFJ': '🎼 인디/로파이 — 사색적이고 감성적인 분위기',
    'INTJ': '🎧 미니멀 테크노 — 고요하고 집중력 있는 사운드',
    'ISTP': '🎸 록 또는 블루스 — 자유롭고 즉흥적인 리듬',
    'ISFP': '🎹 피아노 연주곡, 뉴에이지 — 감성적이고 평화로움',
    'INFP': '🎤 감성 팝/발라드 — 깊은 감정 몰입',
    'INTP': '🧠 앰비언트 전자음악 — 창의적이고 몽환적인 느낌',
    'ESTP': '🔥 펑크, EDM — 에너지 넘치는 활동형 음악',
    'ESFP': '🎉 팝/댄스 — 활발하고 흥겨운 분위기',
    'ENFP': '🌍 월드뮤직, 퓨전 — 다양성과 창의성 가득',
    'ENTP': '🚀 힙합, 얼터너티브 — 도전적이고 혁신적인 스타일',
    'ESTJ': '📻 올드팝, 브라스 밴드 — 리더십과 조직적인 느낌',
    'ESFJ': '🎶 팝 발라드 — 모두가 공감하는 감성',
    'ENFJ': '🎵 뮤지컬 OST — 극적이고 감정 표현이 강한 음악',
    'ENTJ': '🎧 시네마틱 사운드트랙 — 파워풀하고 영감을 주는 음악'
}

mbti_ceos = {
    'ISTJ': ['📈 Jeff Bezos (아마존 창업자)', '🏢 Fred Smith (FedEx 창업자)'],
    'ISFJ': ['🤝 Mother Teresa (자선가)', '💼 Brian Chesky (Airbnb 창업자)'],
    'INFJ': ['📚 Oprah Winfrey (미디어 거물)', '🌿 Chris Hughes (페이스북 공동 창업자)'],
    'INTJ': ['🧠 Mark Zuckerberg (페이스북)', '🚀 Elon Musk (스페이스X, 테슬라)'],
    'ISTP': ['🔧 Steve Wozniak (애플 공동 창업자)', '🛠️ James Dyson (다이슨 창업자)'],
    'ISFP': ['🎨 Bob Ross (미술 교육가)', '🎶 Kanye West (패션/음악 사업가)'],
    'INFP': ['📖 JK Rowling (해리포터 작가/사업가)', '🖌️ Tim Burton (감독/프랜차이즈 사업)'],
    'INTP': ['💡 Larry Page (구글 창업자)', '🧠 Bill Gates (MS 공동 창업자)'],
    'ESTP': ['💼 Donald Trump (부동산 사업가)', '🚗 Richard Branson (버진 그룹)'],
    'ESFP': ['🎤 Beyoncé (아티스트/브랜드)', '🎉 Jamie Oliver (요리사/사업가)'],
    'ENFP': ['🌍 Richard Branson (버진 그룹)', '🎬 Walt Disney (디즈니 창업자)'],
    'ENTP': ['🚀 Elon Musk (테슬라)', '📱 Steve Jobs (애플)'],
    'ESTJ': ['💰 Warren Buffett (버크셔 해서웨이)', '🏛️ Indra Nooyi (펩시 CEO)'],
    'ESFJ': ['💄 Rihanna (Fenty 창업자)', '🎙️ Oprah Winfrey (미디어 사업가)'],
    'ENFJ': ['👩‍🏫 Sheryl Sandberg (전 페이스북 COO)', '🗣️ Barack Obama (정치/리더십)'],
    'ENTJ': ['🚀 Jeff Bezos (아마존)', '📊 Martha Stewart (사업가/방송인)']
}

# ---------------------- 사용자 입력 ----------------------
mbti_list = list(mbti_jobs.keys())
selected_mbti = st.selectbox("🔠 MBTI를 선택하세요", mbti_list)

# ---------------------- 추천 결과 ----------------------
st.markdown(f"## 💼 `{selected_mbti}` 유형에게 어울리는 직업")
cols_jobs = st.columns(3)
for i, job in enumerate(mbti_jobs[selected_mbti]):
    with cols_jobs[i % 3]:
        st.markdown(f'<div class="card">{job}</div>', unsafe_allow_html=True)

st.markdown(f"## 🎵 `{selected_mbti}` 유형에게 추천하는 음악 스타일")
st.markdown(f'<div class="card">{mbti_music[selected_mbti]}</div>', unsafe_allow_html=True)

st.markdown(f"## 👑 `{selected_mbti}` 유형의 대표적인 성공한 인물")
cols_ceos = st.columns(2)
for i, ceo in enumerate(mbti_ceos[selected_mbti]):
    with cols_ceos[i % 2]:
        st.markdown(f'<div class="card">{ceo}</div>', unsafe_allow_html=True)

# ---------------------- 하단 정보 ----------------------
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("✅ 이 앱은 MBTI 기반 진로·음악·롤모델 탐색을 위한 교육용 웹앱입니다.")
st.markdown("🔗 *Made with ❤️ by ChatGPT + Streamlit*")

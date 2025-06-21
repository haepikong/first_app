import streamlit as st
import random

# -------------------- 페이지 설정 --------------------
st.set_page_config(page_title="🎯 이모지 직업 맞추기 게임!", page_icon="🧩", layout="centered")

# -------------------- CSS 스타일 --------------------
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 50px;
            font-weight: bold;
            color: #FF6F61;
        }
        .emoji-box {
            font-size: 60px;
            text-align: center;
            margin: 30px 0;
        }
        .feedback {
            font-size: 30px;
            text-align: center;
            margin: 20px 0;
        }
        .correct {
            color: green;
            font-weight: bold;
        }
        .wrong {
            color: red;
            font-weight: bold;
        }
        .job-box {
            background-color: #FFF8E1;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- 문제 데이터 --------------------
emoji_jobs = {
    "👨‍⚕️💉🩺": "의사",
    "👨‍🍳🍳🥘": "요리사",
    "👮‍♂️🚓🔫": "경찰",
    "👨‍🏫📚🖊️": "교사",
    "👩‍🔬🧪🔬": "과학자",
    "👨‍💻🧑‍💻💻": "프로그래머",
    "👨‍🚀🚀🌌": "우주비행사",
    "👩‍🎤🎤🎶": "가수",
    "🧑‍⚖️⚖️📜": "판사",
    "👩‍🚒🔥🚒": "소방관",
    "🎨🖌️🖼️": "화가",
    "🎥🎬📽️": "감독",
    "📸📷🖼️": "사진작가",
    "✈️👨‍✈️🛩️": "파일럿",
    "💄💅👄": "뷰티아티스트",
    "⚽🏃‍♂️🥅": "축구선수",
    "🎻🎼🎹": "음악가",
    "🧘‍♀️🧘‍♂️🕉️": "요가강사",
    "🛠️🔩🔧": "기술자",
    "🧵🪡👗": "디자이너"
}

TOTAL_QUESTIONS = 20

# -------------------- 상태 초기화 --------------------
if "quiz" not in st.session_state:
    st.session_state.quiz = random.sample(list(emoji_jobs.items()), TOTAL_QUESTIONS)
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.feedback = ""
    st.session_state.show_answer = False
    st.session_state.input = ""

# -------------------- 현재 문제 --------------------
if st.session_state.index < TOTAL_QUESTIONS:
    emoji, answer = st.session_state.quiz[st.session_state.index]

    st.markdown('<div class="title">🧩 이모지 직업 퀴즈</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="emoji-box">{emoji}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="job-box">문제 {st.session_state.index+1} / {TOTAL_QUESTIONS} - 이 이모지가 의미하는 직업은?</div>', unsafe_allow_html=True)

    user_input = st.text_input("✏️ 당신의 정답:", value=st.session_state.input, key="answer_input")

    if st.button("✅ 제출"):
        st.session_state.input = user_input
        if user_input.strip() == answer:
            st.session_state.feedback = f"🎉 정답! '{answer}' 맞습니다!"
            st.session_state.score += 1
            st.session_state.show_answer = True
        else:
            st.session_state.feedback = f"😢 오답! 정답은 '{answer}'였어요."
            st.session_state.show_answer = True

    if st.session_state.show_answer:
        color = "correct" if st.session_state.input == answer else "wrong"
        st.markdown(f'<div class="feedback {color}">{st.session_state.feedback}</div>', unsafe_allow_html=True)

        if st.button("➡️ 다음 문제"):
            st.session_state.index += 1
            st.session_state.feedback = ""
            st.session_state.input = ""
            st.session_state.show_answer = False

# -------------------- 결과 화면 --------------------
else:
    st.markdown('<div class="title">🎉 게임 종료!</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="job-box" style="text-align:center; font-size:28px;">
            당신의 점수는 <b>{st.session_state.score} / {TOTAL_QUESTIONS}</b>입니다!<br><br>
            다시 도전해보시겠어요?
        </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 다시 시작하기"):
        del st.session_state.quiz
        del st.session_state.index
        del st.session_state.score
        del st.session_state.feedback
        del st.session_state.input
        del st.session_state.show_answer

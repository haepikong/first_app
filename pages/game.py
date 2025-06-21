import streamlit as st
import random

# --------------------- 페이지 설정 ---------------------
st.set_page_config(page_title="🎯 이모지 직업 맞추기 게임!", page_icon="🧩", layout="centered")

# --------------------- 스타일 설정 ---------------------
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
        .btn {
            display: block;
            margin: 10px auto;
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------- 데이터셋 ---------------------
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
    "👩‍🚒🔥🚒": "소방관"
}

# --------------------- 상태 저장 ---------------------
if "current_emoji" not in st.session_state:
    st.session_state.current_emoji, st.session_state.answer = random.choice(list(emoji_jobs.items()))
    st.session_state.feedback = ""
    st.session_state.correct = None

# --------------------- 헤더 ---------------------
st.markdown('<div class="title">🎉 이모지로 직업 맞추기!</div>', unsafe_allow_html=True)

# --------------------- 문제 카드 ---------------------
st.markdown(f'<div class="emoji-box">{st.session_state.current_emoji}</div>', unsafe_allow_html=True)
st.markdown('<div class="job-box">아래에 직업을 입력해보세요! (예: 의사, 요리사, 교사 등)</div>', unsafe_allow_html=True)

user_input = st.text_input("✏️ 당신의 정답:", key="answer_input")

# --------------------- 정답 확인 ---------------------
if st.button("✅ 확인하기"):
    if user_input.strip() == st.session_state.answer:
        st.session_state.feedback = f'🎯 정답! {st.session_state.answer} 맞아요!'
        st.session_state.correct = True
    else:
        st.session_state.feedback = f'😢 오답! 정답은 {st.session_state.answer}였어요.'
        st.session_state.correct = False

# --------------------- 피드백 ---------------------
if st.session_state.feedback:
    color = "correct" if st.session_state.correct else "wrong"
    st.markdown(f'<div class="feedback {color}">{st.session_state.feedback}</div>', unsafe_allow_html=True)

# --------------------- 다음 문제 버튼 ---------------------
if st.session_state.feedback:
    if st.button("🔁 다음 문제"):
        st.session_state.current_emoji, st.session_state.answer = random.choice(list(emoji_jobs.items()))
        st.session_state.feedback = ""
        st.session_state.correct = None
        st.session_state.answer_input = ""

# --------------------- 하단 ---------------------
st.markdown("<hr>")
st.markdown("💡 힌트: 이모지를 잘 보고 직업을 상상해보세요!")
st.markdown("📌 *Made with ❤️ by ChatGPT + Streamlit*")


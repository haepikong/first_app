import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.set_page_config(page_title="📈 글로벌 TOP10 주가 추이", layout="wide")

st.title("🌍 글로벌 시가총액 TOP 10 기업의 최근 1년 주가 변화")
st.markdown("📊 데이터 출처: [Yahoo Finance](https://finance.yahoo.com)")

# 시가총액 기준 글로벌 Top 10 기업 티커
top_10_tickers = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Alphabet (GOOGL)": "GOOGL",
    "Amazon (AMZN)": "AMZN",
    "NVIDIA (NVDA)": "NVDA",
    "Berkshire Hathaway (BRK-B)": "BRK-B",
    "Tesla (TSLA)": "TSLA",
    "Meta (META)": "META",
    "Taiwan Semiconductor (TSM)": "TSM",
    "Eli Lilly (LLY)": "LLY"
}

# 날짜 범위 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# 데이터 불러오기
tickers = list(top_10_tickers.values())
data = yf.download(tickers, start=start_date, end=end_date)["Adj Close"]

# Plotly 시각화
fig = go.Figure()

for label, ticker in top_10_tickers.items():
    if ticker in data.columns:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data[ticker],
            mode='lines',
            name=label
        ))

fig.update_layout(
    title="📈 최근 1년 간 주가 추이 (조정 종가 기준)",
    xaxis_title="날짜",
    yaxis_title="주가 (USD)",
    height=600,
    template="plotly_white",
    legend_title="기업"
)

st.plotly_chart(fig, use_container_width=True)


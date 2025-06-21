
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📍 송파구 따릉이 보관소 지도", layout="wide")
st.title("🚲 송파구 따릉이 보관소 위치 시각화")

# 직접 추출한 송파구 대여소 데이터 샘플
data = [
    {"name": "가락시장역 2번 출구", "lat": 37.4955, "lon": 127.1234},
    {"name": "경찰병원역 1번 출구", "lat": 37.4998, "lon": 127.1126},
    {"name": "마천역 1번 출구", "lat": 37.5033, "lon": 127.1525},
    {"name": "석촌고분역 2번 출구", "lat": 37.5050, "lon": 127.1000},
    {"name": "송파파크데일 4단지", "lat": 37.5100, "lon": 127.1150},
    # …더 많은 실제 데이터 추가 가능
]

df = pd.DataFrame(data)

# Plotly로 지도 생성
fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    hover_name="name",
    zoom=13,
    height=700
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r":0,"t":0,"l":0,"b":0}
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
본 지도는 송파구에 설치된 따릉이 대여소 위치를 표시한 예시입니다.  
데이터는 서울 열린데이터광장의 마스터 데이터를 바탕으로 표본화했습니다 :contentReference[oaicite:7]{index=7}.
""")

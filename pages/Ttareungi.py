import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📍 송파구 따릉이 현황 지도", layout="wide")
st.title("🚲 송파구 따릉이 대여소 현황 시각화")
st.markdown("자전거 보관소별 거치대 수와 남은 자전거 수를 색상과 크기로 표시합니다.")

# -- 데이터 불러오기 예시 (CSV 직접 URL로 지정 또는 로컬 업로드) --
@st.cache_data
def load_data():
    # 예시 URL: 실제 CSV 다운로드 URL 필요
    url = "https://…/PublicBikeStationInfo_Songpa.csv"
    df = pd.read_csv(url)
    # columns: ['station_name', 'latitude', 'longitude', 'rack_count', 'available_bikes']
    # 샘플 필터: 송파구에 해당하는 데이터만
    df = df[df['district'] == '송파구']
    return df

# 업로드 방식 예시
uploaded = st.file_uploader("📥 CSV 파일 업로드 (송파구 따릉이 대여소)")
if uploaded:
    df = pd.read_csv(uploaded)
else:
    st.warning("CSV 파일을 업로드해 주세요.")
    st.stop()

# -- 산포도 지도 생성 --
fig = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    hover_name="station_name",
    hover_data={"rack_count":True, "available_bikes":True},
    size="rack_count",
    color="available_bikes",
    color_continuous_scale="Viridis",
    size_max=30,
    zoom=12,
    height=700
)

fig.update_layout(mapbox_style="open-street-map", margin={"t":0,"b":0,"l":0,"r":0})
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
- 🟥 **마커 크기**: 거치대 전체 수  
- 🟦 **마커 색상**: 남은 자전거 수 (진할수록 많음)  
- 📌 지도에서 마커 클릭 시 상세 정보 확인 가능
""")


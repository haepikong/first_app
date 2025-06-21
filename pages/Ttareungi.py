import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="🚲 따릉이 대여소 이용 시각화", layout="wide")
st.title("📍 서울시 따릉이 대여소 이용 현황 지도")
st.markdown("마커의 크기는 총 이용 횟수, 색상은 반납률을 나타냅니다.")

# 파일 업로드
st.subheader("1️⃣ 따릉이 대여소 위치 정보 CSV 업로드")
master_file = st.file_uploader("🗂️ 대여소 마스터 파일 (위도, 경도 포함)", type=["csv"])

st.subheader("2️⃣ 따릉이 대여/반납 승객 수 CSV 업로드")
trip_file = st.file_uploader("🗂️ 대여/반납 이용 정보 파일", type=["csv"])

# 업로드 완료되었을 때 실행
if master_file and trip_file:
    try:
        # 데이터 읽기
        master = pd.read_csv(master_file)
        trip = pd.read_csv(trip_file)

        # 필수 컬럼 존재 여부 확인
        required_master_cols = {"station_id", "station_name", "latitude", "longitude"}
        required_trip_cols = {"station_id", "rental_count", "return_count"}

        if not required_master_cols.issubset(master.columns) or not required_trip_cols.issubset(trip.columns):
            st.error("📛 CSV 파일에 필수 컬럼이 없습니다.")
            st.stop()

        # 데이터 병합
        merged = pd.merge(master, trip, on="station_id", how="left").fillna(0)

        # 파생 컬럼 생성
        merged["total_trips"] = merged["rental_count"] + merged["return_count"]
        merged["return_ratio"] = merged["return_count"] / merged["rental_count"].replace(0, 1)

        # 지도 시각화
        fig = px.scatter_mapbox(
            merged,
            lat="latitude",
            lon="longitude",
            hover_name="station_name",
            hover_data={
                "rental_count": True,
                "return_count": True,
                "total_trips": True,
                "return_ratio": True,
                "latitude": False,
                "longitude": False
            },
            size="total_trips",
            color="return_ratio",
            color_continuous_scale="Viridis",
            size_max=30,
            zoom=11,
            height=700
        )

        fig.update_layout(mapbox_style="open-street-map", margin={"t":0, "b":0, "l":0, "r":0})
        st.plotly_chart(fig, use_container_width=True)

        st.success("✅ 지도 시각화가 완료되었습니다!")

    except Exception as e:
        st.error(f"오류 발생: {e}")
else:
    st.info("⬆️ 위 두 개의 CSV 파일을 모두 업로드해주세요.")

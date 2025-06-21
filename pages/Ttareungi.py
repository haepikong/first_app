import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="🚲 따릉이 대여소 지도 시각화", layout="wide")
st.title("📍 서울시 따릉이 대여소 대여/반납 현황 지도")
st.markdown("두 개의 CSV 파일을 업로드하면 지도에 마커로 현황을 표시합니다.")

# 업로드 안내
st.markdown("### 1️⃣ 따릉이 대여소 위치 정보 CSV")
master_file = st.file_uploader("대여소 마스터 파일 (station_id, station_name, latitude, longitude)", type="csv")

st.markdown("### 2️⃣ 따릉이 대여/반납 통계 CSV")
trip_file = st.file_uploader("대여/반납 통계 파일 (station_id, rental_count, return_count)", type="csv")

# 업로드 후 실행
if master_file and trip_file:
    try:
        # 데이터 읽기
        master = pd.read_csv(master_file)
        trip = pd.read_csv(trip_file)

        # 컬럼명 소문자 처리 및 공백 제거
        master.columns = master.columns.str.strip().str.lower()
        trip.columns = trip.columns.str.strip().str.lower()

        # 필수 컬럼 검사
        master_cols = {'station_id', 'station_name', 'latitude', 'longitude'}
        trip_cols = {'station_id', 'rental_count', 'return_count'}

        if not master_cols.issubset(master.columns):
            missing = master_cols - set(master.columns)
            st.error(f"❌ 마스터 CSV에 다음 컬럼이 없습니다: {missing}")
            st.stop()

        if not trip_cols.issubset(trip.columns):
            missing = trip_cols - set(trip.columns)
            st.error(f"❌ 통계 CSV에 다음 컬럼이 없습니다: {missing}")
            st.stop()

        # 숫자형 컬럼 강제 변환
        trip['rental_count'] = pd.to_numeric(trip['rental_count'], errors='coerce')
        trip['return_count'] = pd.to_numeric(trip['return_count'], errors='coerce')

        # 병합
        df = pd.merge(master, trip, on="station_id", how="left")
        df[['rental_count', 'return_count']] = df[['rental_count', 'return_count']].fillna(0)

        # 파생 컬럼
        df['total_trips'] = df['rental_count'] + df['return_count']
        df['return_ratio'] = df['return_count'] / df['rental_count'].replace(0, 1)

        # 지도 시각화
        fig = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            hover_name="station_name",
            hover_data={
                "rental_count": True,
                "return_count": True,
                "total_trips": True,
                "return_ratio": ":.2f",
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
        st.exception(f"예기치 못한 오류 발생: {e}")
else:
    st.info("⬆️ 위 두 개의 CSV 파일을 모두 업로드해주세요.")

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🚲 따릉이 대여소 지도 시각화", layout="wide")
st.title("📍 서울시 따릉이 대여/반납 현황 지도")

st.markdown("CSV 인코딩 문제, 빈 파일 문제를 방지하고, 업로드한 데이터를 자동 분석하여 지도에 표시합니다.")

# 여러 인코딩 시도 및 에러 방지
def safe_read_csv(uploaded_file):
    encodings = ['utf-8-sig', 'cp949', 'euc-kr', 'latin1']
    for enc in encodings:
        try:
            df = pd.read_csv(uploaded_file, encoding=enc)
            if df.empty or df.shape[1] == 0:
                continue  # 컬럼 없음: 다음 인코딩 시도
            return df
        except Exception:
            continue
    st.error("❌ 파일을 열 수 없습니다. 인코딩 또는 형식을 확인해주세요.")
    return None

# 업로드
st.subheader("1️⃣ 대여소 위치 정보 CSV")
master_file = st.file_uploader("예: station_id, station_name, latitude, longitude 포함", type="csv")

st.subheader("2️⃣ 대여/반납 통계 CSV")
trip_file = st.file_uploader("예: station_id, rental_count, return_count 포함", type="csv")

# 처리
if master_file and trip_file:
    master = safe_read_csv(master_file)
    trip = safe_read_csv(trip_file)

    if master is None or trip is None:
        st.stop()

    # 컬럼 자동 정리
    master.columns = master.columns.str.strip().str.lower()
    trip.columns = trip.columns.str.strip().str.lower()

    # 컬럼 유효성 검사
    master_cols = {"station_id", "station_name", "latitude", "longitude"}
    trip_cols = {"station_id", "rental_count", "return_count"}

    if not master_cols.issubset(master.columns):
        st.error(f"📛 마스터 CSV에 다음 컬럼이 없습니다: {master_cols - set(master.columns)}")
        st.write("🔍 업로드한 파일:", master.head())
        st.stop()

    if not trip_cols.issubset(trip.columns):
        st.error(f"📛 통계 CSV에 다음 컬럼이 없습니다: {trip_cols - set(trip.columns)}")
        st.write("🔍 업로드한 파일:", trip.head())
        st.stop()

    # 숫자 변환
    trip['rental_count'] = pd.to_numeric(trip['rental_count'], errors='coerce')
    trip['return_count'] = pd.to_numeric(trip['return_count'], errors='coerce')

    # 병합
    df = pd.merge(master, trip, on="station_id", how="left")
    df[['rental_count', 'return_count']] = df[['rental_count', 'return_count']].fillna(0)
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
            "return_ratio": ':.2f'
        },
        size="total_trips",
        color="return_ratio",
        color_continuous_scale="Viridis",
        size_max=30,
        zoom=11,
        height=700
    )
    fig.update_layout(mapbox_style="open-street-map", margin={"t": 0, "b": 0, "l": 0, "r": 0})
    st.plotly_chart(fig, use_container_width=True)
    st.success("✅ 지도 시각화 완료!")

else:
    st.info("⬆️ 두 개의 CSV 파일을 모두 업로드해주세요.")

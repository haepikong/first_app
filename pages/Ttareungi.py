import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🚲 따릉이 지도 시각화", layout="wide")
st.title("📍 서울시 따릉이 대여소 현황 시각화")
st.markdown("✔️ 마커 크기는 총 이용 횟수, 색상은 반납률입니다.")

# ⚙️ 안전하게 여러 인코딩 시도하며 CSV 읽기
def safe_read_csv(uploaded_file):
    encodings = ['utf-8-sig', 'utf-8', 'cp949', 'euc-kr', 'latin1']
    for enc in encodings:
        try:
            df = pd.read_csv(uploaded_file, encoding=enc)
            if df.empty or df.shape[1] == 0:
                continue
            return df
        except Exception:
            continue
    return pd.DataFrame()  # 아무것도 못 읽으면 빈 DataFrame 반환

# 📁 파일 업로드
st.subheader("1️⃣ 대여소 위치 정보 CSV")
master_file = st.file_uploader("station_id, station_name, latitude, longitude 컬럼 포함", type="csv")

st.subheader("2️⃣ 대여/반납 통계 CSV")
trip_file = st.file_uploader("station_id, rental_count, return_count 컬럼 포함", type="csv")

if master_file and trip_file:
    master = safe_read_csv(master_file)
    trip = safe_read_csv(trip_file)

    if master.empty or trip.empty:
        st.warning("⚠️ 업로드된 파일을 읽을 수 없습니다. Excel에서 **CSV UTF-8(콤마로 분리)** 형식으로 다시 저장해보세요.")
        st.stop()

    # ✅ 컬럼명 정리
    master.columns = master.columns.str.strip().str.lower()
    trip.columns = trip.columns.str.strip().str.lower()

    # ✅ 필수 컬럼 존재 여부 확인
    master_cols = {"station_id", "station_name", "latitude", "longitude"}
    trip_cols = {"station_id", "rental_count", "return_count"}

    if not master_cols.issubset(master.columns):
        st.error(f"❌ 마스터 파일에 누락된 컬럼: {master_cols - set(master.columns)}")
        st.write(master.head())
        st.stop()

    if not trip_cols.issubset(trip.columns):
        st.error(f"❌ 통계 파일에 누락된 컬럼: {trip_cols - set(trip.columns)}")
        st.write(trip.head())
        st.stop()

    # ✅ 숫자형으로 변환
    trip['rental_count'] = pd.to_numeric(trip['rental_count'], errors='coerce').fillna(0)
    trip['return_count'] = pd.to_numeric(trip['return_count'], errors='coerce').fillna(0)

    # ✅ 병합 및 파생 컬럼 생성
    df = pd.merge(master, trip, on="station_id", how="left").fillna(0)
    df['total_trips'] = df['rental_count'] + df['return_count']
    df['return_ratio'] = df['return_count'] / df['rental_count'].replace(0, 1)

    # ✅ 지도 시각화
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
    st.info("⬆️ 위 두 개의 CSV 파일을 업로드해주세요.")

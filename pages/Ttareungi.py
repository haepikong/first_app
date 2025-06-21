import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🚲 따릉이 대여소 지도 시각화", layout="wide")
st.title("📍 서울시 따릉이 대여소 대여/반납 현황 지도")

st.markdown("마커 크기: 총 이용 횟수 / 색상: 반납률")

# CSV 안전 읽기 함수
def safe_read_csv(uploaded_file):
    try:
        return pd.read_csv(uploaded_file, encoding='utf-8-sig')
    except UnicodeDecodeError:
        try:
            return pd.read_csv(uploaded_file, encoding='cp949')
        except Exception as e:
            st.error(f"❌ 파일 인코딩 문제로 읽을 수 없습니다: {e}")
            return None

# 파일 업로드
st.markdown("### 📂 대여소 위치 정보 CSV")
master_file = st.file_uploader("station_id, station_name, latitude, longitude 컬럼이 포함되어야 합니다.", type="csv")

st.markdown("### 📂 대여/반납 통계 CSV")
trip_file = st.file_uploader("station_id, rental_count, return_count 컬럼이 포함되어야 합니다.", type="csv")

if master_file and trip_file:
    master = safe_read_csv(master_file)
    trip = safe_read_csv(trip_file)

    if master is not None and trip is not None:
        try:
            # 컬럼 정리
            master.columns = master.columns.str.strip().str.lower()
            trip.columns = trip.columns.str.strip().str.lower()

            # 필수 컬럼 검사
            master_cols = {"station_id", "station_name", "latitude", "longitude"}
            trip_cols = {"station_id", "rental_count", "return_count"}

            if not master_cols.issubset(master.columns):
                missing = master_cols - set(master.columns)
                st.error(f"❌ 마스터 파일에 다음 컬럼이 없습니다: {missing}")
                st.stop()

            if not trip_cols.issubset(trip.columns):
                missing = trip_cols - set(trip.columns)
                st.error(f"❌ 통계 파일에 다음 컬럼이 없습니다: {missing}")
                st.stop()

            # 숫자 변환
            trip["rental_count"] = pd.to_numeric(trip["rental_count"], errors="coerce")
            trip["return_count"] = pd.to_numeric(trip["return_count"], errors="coerce")

            # 병합 및 처리
            df = pd.merge(master, trip, on="station_id", how="left")
            df[["rental_count", "return_count"]] = df[["rental_count", "return_count"]].fillna(0)
            df["total_trips"] = df["rental_count"] + df["return_count"]
            df["return_ratio"] = df["return_count"] / df["rental_count"].replace(0, 1)

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
                    "return_ratio": ":.2f"
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
            st.success("✅ 시각화 완료!")

        except Exception as e:
            st.exception(f"❌ 예기치 못한 오류: {e}")
    else:
        st.warning("📛 CSV 파일을 제대로 읽을 수 없습니다. 인코딩을 확인해 주세요.")
else:
    st.info("⬆️ 두 개의 CSV 파일을 업로드해주세요.")

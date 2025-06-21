import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🚲 따릉이 지도 시각화", layout="wide")
st.title("📍 서울시 따릉이 대여소 현황 시각화")

st.markdown("✔️ 마커 크기는 총 이용 횟수, 색상은 반납률입니다.")

# 안전한 CSV 읽기 함수
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
    return pd.DataFrame()  # 실패 시 빈 DataFrame 반환

# 파일 업로드
st.subheader("1️⃣ 대여소 위치 정보 CSV")
master_file = st.file_uploader("📁 station_id, station_name, latitude, longitude 컬럼 포함", type="csv")

st.subheader("2️⃣ 대여/반납 통계 CSV")
trip_file = st.file_uploader("📁 station_id, rental_count, return_count 컬럼 포함", type="csv")

if master_file and trip_file:
    master = safe_read_csv(master_file)
    trip = safe_read_csv(trip_file)

    if master.empty or trip.empty:
        st.warning("⚠️ 파일이 비어 있거나 읽을 수 없습니다. 엑셀에서 'CSV UTF-8' 형식으로 저장해보세요.")
    else:
        # 컬럼 정리
        master.columns = master.columns.str.strip().str.lower()
        trip.columns = trip.columns.str.strip().str.lower()

        # 필수 컬럼 정의
        master_cols_required = {"station_id", "station_name", "latitude", "longitude"}
        trip_cols_required = {"station_id", "rental_count", "return_count"}

        # 누락된 컬럼 확인 및 알림
        master_missing = master_cols_required - set(master.columns)
        trip_missing = trip_cols_required - set(trip.columns)

        if master_missing:
            st.warning(f"⚠️ 마스터 파일에서 누락된 컬럼: {master_missing}")
        if trip_missing:
            st.warning(f"⚠️ 통계 파일에서 누락된 컬럼: {trip_missing}")

        st.subheader("✅ 업로드된 마스터 데이터 미리보기")
        st.write(master.head())

        st.subheader("✅ 업로드된 통계 데이터 미리보기")
        st.write(trip.head())

        # 필수 컬럼이 모두 존재할 경우에만 시각화
        if not master_missing and not trip_missing:
            # 숫자 변환
            trip['rental_count'] = pd.to_numeric(trip['rental_count'], errors='coerce').fillna(0)
            trip['return_count'] = pd.to_numeric(trip['return_count'], errors='coerce').fillna(0)

            # 병합 및 계산
            df = pd.merge(master, trip, on="station_id", how="left").fillna(0)
            df['total_trips'] = df['rental_count'] + df['return_count']
            df['return_ratio'] = df['return_count'] / df['rental_count'].replace(0, 1)

            # 시각화
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
            st.info("💡 지도 시각화를 위해 마스터와 통계 파일의 필수 컬럼이 모두 필요합니다.")
else:
    st.info("⬆️ 두 개의 CSV 파일을 업로드해주세요.")

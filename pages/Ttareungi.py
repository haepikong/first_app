import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🚲 따릉이 지도 시각화", layout="wide")
st.title("📍 서울시 따릉이 대여소 현황 시각화")

st.markdown("✔️ 마커 크기는 총 이용 횟수, 색상은 반납률입니다.")

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
    return pd.DataFrame()

# 파일 업로드
st.subheader("1️⃣ 대여소 위치 정보 CSV")
master_file = st.file_uploader("station_id, station_name, latitude, longitude 컬럼 포함", type="csv")

st.subheader("2️⃣ 대여/반납 통계 CSV")
trip_file = st.file_uploader("station_id, rental_count, return_count 컬럼 포함", type="csv")

master = safe_read_csv(master_file) if master_file else pd.DataFrame()
trip = safe_read_csv(trip_file) if trip_file else pd.DataFrame()

if master.empty and trip.empty:
    st.info("⬆️ 두 개의 CSV 파일 중 최소 한 개 이상 업로드해주세요.")
else:
    # 컬럼 정리
    master.columns = master.columns.str.strip().str.lower() if not master.empty else pd.Index([])
    trip.columns = trip.columns.str.strip().str.lower() if not trip.empty else pd.Index([])

    # 필수 컬럼 정의
    master_cols = {"station_id", "station_name", "latitude", "longitude"}
    trip_cols = {"station_id", "rental_count", "return_count"}

    # 누락 컬럼 탐색
    master_missing = master_cols - set(master.columns) if not master.empty else master_cols
    trip_missing = trip_cols - set(trip.columns) if not trip.empty else trip_cols

    # 경고 출력
    if master_file and master_missing:
        st.warning(f"⚠️ 마스터 파일 누락 컬럼: {master_missing}")
    if trip_file and trip_missing:
        st.warning(f"⚠️ 통계 파일 누락 컬럼: {trip_missing}")

    # 데이터 병합 가능 여부 확인
    can_merge = (not master.empty and not trip.empty and
                 not master_missing and not trip_missing)

    # 데이터 준비
    if can_merge:
        trip['rental_count'] = pd.to_numeric(trip['rental_count'], errors='coerce').fillna(0)
        trip['return_count'] = pd.to_numeric(trip['return_count'], errors='coerce').fillna(0)
        df = pd.merge(master, trip, on="station_id", how="left").fillna(0)
    elif not master.empty and not master_missing:
        # 통계 없으면 대여소 위치만 사용, 빈 컬럼 채움
        df = master.copy()
        df['rental_count'] = 0
        df['return_count'] = 0
    elif not trip.empty and not trip_missing:
        # 위치 없으면 통계만, 위도/경도 더미값 넣기 (표시 불가)
        df = trip.copy()
        df['latitude'] = None
        df['longitude'] = None
        df['station_name'] = df['station_id']  # 이름 대체
    else:
        st.error("❌ 시각화에 필요한 최소한의 데이터가 없습니다.")
        st.stop()

    # 파생 컬럼
    df['total_trips'] = df.get('rental_count', 0) + df.get('return_count', 0)
    df['return_ratio'] = df['return_count'] / df['rental_count'].replace(0, 1)

    # 지도 시각화 (위도/경도 없으면 안내)
    if df['latitude'].isnull().all() or df['longitude'].isnull().all():
        st.warning("⚠️ 위치 정보가 없어서 지도에 표시할 수 없습니다. 위치정보가 포함된 CSV를 함께 업로드해주세요.")
    else:
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
            size="total_trips" if 'total_trips' in df.columns else None,
            color="return_ratio" if 'return_ratio' in df.columns else None,
            color_continuous_scale="Viridis",
            size_max=30,
            zoom=11,
            height=700
        )
        fig.update_layout(mapbox_style="open-street-map", margin={"t":0,"b":0,"l":0,"r":0})
        st.plotly_chart(fig, use_container_width=True)
        st.success("✅ 지도 시각화 완료!")

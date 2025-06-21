import streamlit as st
import pandas as pd
import zipfile
import io
import plotly.express as px

st.set_page_config(page_title="🚲 서울시 따릉이 이용 지도", layout="wide")
st.title("📍 서울 따릉이 대여소 이용 현황")

# — 데이터 업로드 UI
master_file = st.file_uploader("1️⃣ 대여소 마스터 CSV 업로드", type=["csv"])
trip_file = st.file_uploader("2️⃣ 대여/반납 승객수 ZIP 또는 CSV 업로드", type=["zip","csv"])

if not master_file or not trip_file:
    st.info("각각의 데이터 파일을 업로드해주세요.")
    st.stop()

# — 마스터 정보 로드
master = pd.read_csv(master_file)
# master columns 포함 예: ['station_id','station_name','latitude','longitude']

# — 승객수 데이터 로드 (ZIP 또는 CSV)
if trip_file.name.endswith(".zip"):
    z = zipfile.ZipFile(io.BytesIO(trip_file.read()))
    # ZIP 안에 단일 CSV 가정
    name = z.namelist()[0]
    trip = pd.read_csv(z.open(name))
else:
    trip = pd.read_csv(trip_file)

# trip 컬럼 예: ['station_id','rental_count','return_count']
# — 필요 컬럼만 추출
cols = ['station_id','rental_count','return_count']
trip = trip[cols].groupby('station_id', as_index=False).sum()

# — 마스터 + 통계 데이터 병합
df = master.merge(trip, on='station_id', how='left').fillna(0)

# — 파생 지표 계산
df['total_trips'] = df['rental_count'] + df['return_count']
df['return_ratio'] = df['return_count'] / df['rental_count'].replace(0,1)

# — 지도 시각화
fig = px.scatter_mapbox(
    df,
    lat='latitude', lon='longitude',
    hover_name='station_name',
    hover_data=['rental_count','return_count','return_ratio','total_trips'],
    size='total_trips', color='return_ratio',
    color_continuous_scale='Turbo',
    size_max=40,
    zoom=11,
    height=700
)
fig.update_layout(mapbox_style="open-street-map", margin={'l':0,'r':0,'t':0,'b':0})
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
- 🔵 **마커 크기**: 총 이용 건수(대여+반납)
- 🔴 **색상 진할수록 반납률 높음**
- 📊 마커 클릭 시 상세 이용 정보 확인 가능
""")

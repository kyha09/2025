import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import math

# -----------------------------
# 지점 이름 → 좌표 매핑
# -----------------------------
LOCATION_DICT = {
    "서울시청": (37.5665, 126.9780),
    "강남역": (37.4979, 127.0276),
    "홍대입구역": (37.5572, 126.9238),
    "잠실역": (37.5133, 127.1002),
    "부산시청": (35.1796, 129.0756),
    "대구시청": (35.8714, 128.6014)
}

# -----------------------------
# 원(반경 표시용) 좌표 생성 함수
# -----------------------------
def circle_polygon(lat, lon, radius_m, n=60):
    pts = []
    for i in range(n):
        theta = 2 * math.pi * i / n
        dlat = (radius_m/111_000) * math.cos(theta)
        dlon = (radius_m/(111_000*max(math.cos(math.radians(lat)), 1e-6))) * math.sin(theta)
        pts.append([lon + dlon, lat + dlat])
    pts.append(pts[0])
    return pts

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="범죄 예측 데모", layout="wide")
st.title("📍 지점 기반 범죄예측 데모")

# 지점 선택
place_name = st.selectbox("분석할 지점을 선택하세요", list(LOCATION_DICT.keys()))
center_lat, center_lon = LOCATION_DICT[place_name]

# 반경 선택
radius_m = st.slider("반경 (m)", 100, 3000, 800, step=100)

st.write(f"선택된 지점: **{place_name}** ({center_lat:.4f}, {center_lon:.4f})")

# -----------------------------
# 샘플 데이터 (랜덤 사건 좌표 생성)
# 실제로는 CSV 업로드해서 사용
# -----------------------------
np.random.seed(42)
data = pd.DataFrame({
    "lat": center_lat + np.random.randn(200) * 0.01,
    "lon": center_lon + np.random.randn(200) * 0.01
})

# -----------------------------
# 지도 표시
# -----------------------------
# 히트맵 레이어
heatmap_layer = pdk.Layer(
    "HeatmapLayer",
    data=data,
    get_position='[lon, lat]',
    radiusPixels=40,
    opacity=0.7
)

# 선택 지점 (검은 점)
center_layer = pdk.Layer(
    "ScatterplotLayer",
    data=pd.DataFrame({"lat":[center_lat], "lon":[center_lon]}),
    get_position='[lon, lat]',
    get_fill_color=[0, 0, 0, 255],
    get_radius=10
)

# 반경 원
circle_layer = pdk.Layer(
    "PolygonLayer",
    data=[{"polygon": circle_polygon(center_lat, center_lon, radius_m)}],
    get_polygon="polygon",
    stroked=True,
    filled=False,
    get_line_color=[255, 0, 0],
    line_width_min_pixels=2
)

# 뷰 설정
view_state = pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=13, pitch=0)

# 지도 렌더링
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=view_state,
    layers=[heatmap_layer, center_layer, circle_layer],
    tooltip={"text": f"{place_name} 중심\n빨간 원 = 반경 {radius_m}m"}
))

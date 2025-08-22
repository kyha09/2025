# streamlit_app.py
# ---------------------------------------------------------------
# 스트림릿 앱: 범죄 이동 경로를 바탕으로 다음 범죄 발생 가능 지점 예측
# ---------------------------------------------------------------

import streamlit as st
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt, atan2, degrees
from sklearn.neighbors import KernelDensity
import pydeck as pdk

# ===================== 유틸 함수 ===================== #
EARTH_R = 6371000.0  # meters

def haversine_m(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return EARTH_R * c


def inverse_project_local_xy(lat_ref, lon_ref, mx, my):
    dlat = my / 111_320
    dlon = mx / (111_320 * cos(radians(lat_ref)))
    return lat_ref + dlat, lon_ref + dlon

# ===================== 예측 모델 (간단 CV) ===================== #

def predict_next(df):
    if len(df) < 2:
        return None
    last = df.iloc[-1]
    prev = df.iloc[-2]
    dist = haversine_m(prev.lat, prev.lon, last.lat, last.lon)
    bearing = atan2(last.lon - prev.lon, last.lat - prev.lat)
    dx, dy = dist * sin(bearing), dist * cos(bearing)
    pred_lat, pred_lon = inverse_project_local_xy(last.lat, last.lon, dx, dy)
    return dict(lat=pred_lat, lon=pred_lon, radius_m=200)

# ===================== 샘플 데이터 ===================== #

def make_sample(n=20, start=(37.5665, 126.9780)):
    lat, lon = start
    ts0 = pd.Timestamp("2025-07-01 20:00:00")
    rows = []
    for i in range(n):
        lat += 0.0001 + np.random.normal(0, 0.00005)
        lon += 0.0001 + np.random.normal(0, 0.00005)
        rows.append((ts0 + pd.Timedelta(minutes=10*i), lat, lon))
    return pd.DataFrame(rows, columns=["timestamp", "lat", "lon"])

# ===================== UI ===================== #

st.title("🛰️ 범죄 경로 추적 & 예측 장소 시각화")
st.caption("범인이 지나온 경로를 바탕으로 다음 범죄 발생 가능 지점을 예측합니다.")

file = st.file_uploader("CSV 업로드 (timestamp, lat, lon)", type=["csv"])
if file:
    df = pd.read_csv(file)
else:
    df = make_sample()

# timestamp 처리
if not np.issubdtype(df['timestamp'].dtype, np.datetime64):
    try:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    except:
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

pred = predict_next(df)

# ===================== 지도 시각화 ===================== #

mid_lat, mid_lon = float(df['lat'].mean()), float(df['lon'].mean())
path_data = df[['lat','lon']].rename(columns={'lat':'LAT','lon':'LON'})
pred_point = pd.DataFrame([[pred['lat'], pred['lon']]], columns=['LAT','LON']) if pred else None

layers = []
# 이동 경로
layers.append(
    pdk.Layer(
        "PathLayer",
        data=[{"path": path_data[['LON','LAT']].values.tolist()}],
        get_path="path",
        get_color=[0, 100, 255],
        width_scale=1,
        width_min_pixels=3
    )
)

# 이동 지점들
layers.append(
    pdk.Layer(
        "ScatterplotLayer",
        data=path_data,
        get_position='[LON, LAT]',
        get_radius=40,
        get_fill_color=[0, 180, 255],
        pickable=True
    )
)

# 예측 지점
if pred_point is not None:
    layers.append(
        pdk.Layer(
            "ScatterplotLayer",
            data=pred_point,
            get_position='[LON, LAT]',
            get_radius=80,
            get_fill_color=[255, 0, 0],
            pickable=True
        )
    )

    # 예측 반경 원
    num_circle_pts = 60
    angles = np.linspace(0, 2*np.pi, num_circle_pts, endpoint=False)
    lat_ref, lon_ref = float(pred['lat']), float(pred['lon'])
    ring = []
    for a in angles:
        dx = pred['radius_m'] * np.cos(a)
        dy = pred['radius_m'] * np.sin(a)
        la, lo = inverse_project_local_xy(lat_ref, lon_ref, dx, dy)
        ring.append([lo, la])
    ring.append(ring[0])
    layers.append(
        pdk.Layer(
            "PolygonLayer",
            data=[{"polygon": ring}],
            get_polygon="polygon",
            get_fill_color=[255, 0, 0, 50],
            get_line_color=[200, 0, 0],
            line_width_min_pixels=2
        )
    )

view_state = pdk.ViewState(latitude=mid_lat, longitude=mid_lon, zoom=12)
st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/light-v9", initial_view_state=view_state, layers=layers))

if pred:
    st.success(f"예상 범죄 장소 좌표: ({pred['lat']:.5f}, {pred['lon']:.5f}) ± {pred['radius_m']}m")


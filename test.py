import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np

st.title("🕵️‍♂️ 범죄 경로 추적 & 다음 장소 예측")

# 세션 상태 초기화
if "crime_path" not in st.session_state:
    st.session_state["crime_path"] = []

st.sidebar.header("📍 장소 추가하기")
lat = st.sidebar.number_input("위도 입력", value=37.5665, format="%.6f")
lon = st.sidebar.number_input("경도 입력", value=126.9780, format="%.6f")
if st.sidebar.button("장소 추가"):
    st.session_state["crime_path"].append((lat, lon))

# 데이터프레임으로 변환
path_df = pd.DataFrame(st.session_state["crime_path"], columns=["lat", "lon"])

# 예측 지점 계산 (단순 등속도 외삽)
pred_point = None
if len(path_df) >= 2:
    last = path_df.iloc[-1]
    prev = path_df.iloc[-2]
    lat_diff = last["lat"] - prev["lat"]
    lon_diff = last["lon"] - prev["lon"]
    pred_point = {"lat": last["lat"] + lat_diff, "lon": last["lon"] + lon_diff}

# 지도 Layer
layers = []

# 이동 경로
if not path_df.empty:
    layers.append(pdk.Layer(
        "PathLayer",
        data=[{"path": path_df[["lon", "lat"]].values.tolist()}],
        get_color=[0, 0, 255],
        width_scale=10,
        width_min_pixels=2,
    ))
    layers.append(pdk.Layer(
        "ScatterplotLayer",
        data=path_df,
        get_position='[lon, lat]',
        get_color='[0, 0, 200]',
        get_radius=80,
    ))

# 예측 지점
if pred_point:
    pred_df = pd.DataFrame([pred_point])
    layers.append(pdk.Layer(
        "ScatterplotLayer",
        data=pred_df,
        get_position='[lon, lat]',
        get_color='[200, 0, 0]',
        get_radius=150,
    ))

# 지도 표시
view_state = pdk.ViewState(
    latitude=lat,
    longitude=lon,
    zoom=11,
    pitch=0,
)

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=view_state,
    layers=layers
))

# 현재 경로와 예측 결과 표시
st.subheader("📊 현재 경로 데이터")
st.write(path_df)

if pred_point:
    st.subheader("🔮 예측된 다음 범죄 장소")
    st.write(pred_point)



import streamlit as st
from PIL import Image
import numpy as np
import os
import pandas as pd
import math

# ======================================================
# CONFIG STREAMLIT
# ======================================================
st.set_page_config(layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_image(path):
    full_path = os.path.join(BASE_DIR, path)
    if not os.path.exists(full_path):
        st.error(f"❌ Arquivo não encontrado: {full_path}")
        st.stop()
    return Image.open(full_path)

# ======================================================
# LOAD MAP + PLANE
# ======================================================
map_bg = load_image("data/tiles/map_base.png").convert("RGB")
map_arr_base = np.array(map_bg)

plane_raw = load_image("assets/plane2.png").convert("RGB")
PLANE_SIZE = 64
plane = plane_raw.resize((PLANE_SIZE, PLANE_SIZE))
plane_arr = np.array(plane)
pw, ph = PLANE_SIZE, PLANE_SIZE

MAP_H, MAP_W, _ = map_arr_base.shape

# ======================================================
# REAL MAP GEOREFERENCE (Guarulhos image bounds)
# ======================================================
lat_max = -23.4300
lat_min = -23.5000
lon_min = -46.5100
lon_max = -46.4400

def latlon_to_pixel(lat, lon):
    x = (lon - lon_min) / (lon_max - lon_min) * MAP_W
    y = (lat_max - lat) / (lat_max - lat_min) * MAP_H
    return int(x), int(y)

# ======================================================
# LOAD AIRPORT DATABASE
# ======================================================
airports = pd.read_csv(os.path.join(BASE_DIR, "data/airports.csv"))

# ======================================================
# GAME STATE
# ======================================================
if "offset_x" not in st.session_state:
    st.session_state.offset_x = 0
if "offset_y" not in st.session_state:
    st.session_state.offset_y = 0
if "speed" not in st.session_state:
    st.session_state.speed = 10

VIEW_W = 900
VIEW_H = 600

# ======================================================
# LAYOUT
# ======================================================
col1, col2 = st.columns([1, 4])

# ======================================================
# LEFT PANEL
# ======================================================
with col1:
    st.markdown("### 🛫 Flight Plan")

    origem = st.selectbox("Origem (ICAO):", airports["ICAO"])
    destino = st.selectbox("Destino (ICAO):", airports["ICAO"])

    # Fetch lat/lon of selected airports
    o_lat, o_lon = airports[airports["ICAO"] == origem][["Lat", "Lon"]].values[0]
    d_lat, d_lon = airports[airports["ICAO"] == destino][["Lat", "Lon"]].values[0]

    # Convert to map pixels
    ox_pix, oy_pix = latlon_to_pixel(o_lat, o_lon)
    dx_pix, dy_pix = latlon_to_pixel(d_lat, d_lon)

    # Controls
    st.markdown("### 🕹️ Controles")
    if st.button("Acelerar"):
        st.session_state.speed += 1
    if st.button("Desacelerar"):
        st.session_state.speed = max(1, st.session_state.speed - 1)
    if st.button("Esquerda"):
        st.session_state.offset_x += st.session_state.speed
    if st.button("Direita"):
        st.session_state.offset_x -= st.session_state.speed
    if st.button("Frente"):
        st.session_state.offset_y += st.session_state.speed
    if st.button("Trás"):
        st.session_state.offset_y -= st.session_state.speed

# ======================================================
# RIGHT PANEL — MAP + ROUTE
# ======================================================
with col2:
    st.markdown("## 🗺️ Navegação Real com Rota")

    ox = int(st.session_state.offset_x)
    oy = int(st.session_state.offset_y)

    # clamp
    ox = max(0, min(ox, MAP_W - VIEW_W))
    oy = max(0, min(oy, MAP_H - VIEW_H))

    st.session_state.offset_x = ox
    st.session_state.offset_y = oy

    # Camera view
    view = map_arr_base[oy:oy+VIEW_H, ox:ox+VIEW_W].copy()

    # Draw origin/destination markers
    import cv2

    # relative coords inside VIEW
    o_x_rel = ox_pix - ox
    o_y_rel = oy_pix - oy
    d_x_rel = dx_pix - ox
    d_y_rel = dy_pix - oy

    # Draw markers
    cv2.circle(view, (o_x_rel, o_y_rel), 8, (0,0,255), -1)
    cv2.circle(view, (d_x_rel, d_y_rel), 8, (0,255,0), -1)

    # Draw route line
    cv2.line(view, (o_x_rel, o_y_rel), (d_x_rel, d_y_rel), (255,0,0), 3)

    # Draw plane (centered)
    plane_x = VIEW_W // 2 - pw // 2
    plane_y = VIEW_H // 2 - ph // 2
    view[plane_y:plane_y+ph, plane_x:plane_x+pw] = plane_arr

    st.image(view, use_column_width=True)

# ======================================================
# INFO PANEL
# ======================================================
st.markdown("---")
st.write(f"Velocidade: **{st.session_state.speed}**")
st.write(f"Camera Offset: **({st.session_state.offset_x}, {st.session_state.offset_y})**")
st.write(f"Origem: {origem}  →  Destino: {destino}")

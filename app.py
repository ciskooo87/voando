import streamlit as st
from PIL import Image
import numpy as np
import os

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
# LOAD ASSETS (MAP + PLANE)
# ======================================================
map_bg = load_image("data/tiles/map_base.png").convert("RGB")
map_arr = np.array(map_bg)

plane_raw = load_image("assets/plane2.png").convert("RGB")

# 🔥 Resize airplane
PLANE_SIZE = 64
plane = plane_raw.resize((PLANE_SIZE, PLANE_SIZE))
plane_arr = np.array(plane)
pw, ph = PLANE_SIZE, PLANE_SIZE

# ======================================================
# GAME STATE
# ======================================================
if "offset_x" not in st.session_state:
    st.session_state.offset_x = 0

if "offset_y" not in st.session_state:
    st.session_state.offset_y = 0

if "speed" not in st.session_state:
    st.session_state.speed = 10

# Canvas de visualização
VIEW_W = 900
VIEW_H = 600

# ======================================================
# LAYOUT
# ======================================================
col1, col2 = st.columns([1, 4])

# ======================================================
# CONTROLES
# ======================================================
with col1:
    st.markdown("### 🕹️ Controles")

    if st.button("Acelerar ⬆️"):
        st.session_state.speed += 1

    if st.button("Desacelerar ⬇️"):
        st.session_state.speed = max(1, st.session_state.speed - 1)

    if st.button("Esquerda ⬅️"):
        st.session_state.offset_x -= st.session_state.speed * -1

    if st.button("Direita ➡️"):
        st.session_state.offset_x += st.session_state.speed * -1

    if st.button("Frente ↑"):
        st.session_state.offset_y += st.session_state.speed * -1

    if st.button("Trás ↓"):
        st.session_state.offset_y -= st.session_state.speed * -1

# ======================================================
# CAMERA TRACKING (MAPA SCROLL)
# ======================================================
with col2:
    st.markdown("## 🛫 FlightBuilder2D – Mapa com Scroll Dinâmico")

    ox = int(st.session_state.offset_x)
    oy = int(st.session_state.offset_y)

    # 🔥 Proteger limites do mundo
    ox = max(0, min(ox, map_arr.shape[1] - VIEW_W))
    oy = max(0, min(oy, map_arr.shape[0] - VIEW_H))

    st.session_state.offset_x = ox
    st.session_state.offset_y = oy

    # 🔥 Recorte do mapa (camera view)
    view = map_arr[oy:oy+VIEW_H, ox:ox+VIEW_W].copy()

    # 🔥 Avião sempre no centro
    plane_x = VIEW_W // 2 - pw // 2
    plane_y = VIEW_H // 2 - ph // 2

    view[plane_y:plane_y+ph, plane_x:plane_x+pw] = plane_arr

    st.image(view, use_column_width=True)

# ======================================================
# HUD
# ======================================================
st.markdown("---")
st.write(f"Velocidade: **{st.session_state.speed} nós**")
st.write(f"Offset X: **{st.session_state.offset_x}**")
st.write(f"Offset Y: **{st.session_state.offset_y}**")

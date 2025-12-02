import streamlit as st
from PIL import Image
import numpy as np
import os

st.set_page_config(layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_image(path):
    full_path = os.path.join(BASE_DIR, path)
    if not os.path.exists(full_path):
        st.error(f"❌ Arquivo não encontrado: " + full_path)
        st.stop()
    return Image.open(full_path)

# ======================================================
# LOAD ASSETS (CONVERT TO RGB)
# ======================================================
plane = load_image("assets/plane2.png").convert("RGB")
map_bg = load_image("data/tiles/map_base.png").convert("RGB")

map_arr_base = np.array(map_bg)  # canvas base

# ======================================================
# GAME STATE
# ======================================================
if "x" not in st.session_state:
    st.session_state.x = 400
if "y" not in st.session_state:
    st.session_state.y = 300
if "speed" not in st.session_state:
    st.session_state.speed = 5

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
        st.session_state.x -= st.session_state.speed

    if st.button("Direita ➡️"):
        st.session_state.x += st.session_state.speed

    if st.button("Frente ↑"):
        st.session_state.y -= st.session_state.speed

    if st.button("Trás ↓"):
        st.session_state.y += st.session_state.speed

# ======================================================
# TELA DO JOGO
# ======================================================
with col2:

    st.markdown("## 🛫 FlightBuilder2D – MVP Jogável")

    canvas = map_arr_base.copy()

    px = int(st.session_state.x)
    py = int(st.session_state.y)

    pw, ph = plane.size

    H, W, _ = canvas.shape

    # Proteção de borda
    px = max(0, min(px, W - pw))
    py = max(0, min(py, H - ph))

    st.session_state.x = px
    st.session_state.y = py

    # AVIÃO EM RGB → ARRAY
    plane_arr = np.array(plane)

    # Inserção segura
    canvas[py:py+ph, px:px+pw] = plane_arr

    st.image(canvas, use_column_width=True)

# ======================================================
# PAINEL
# ======================================================
st.markdown("---")
st.write(f"Velocidade: **{st.session_state.speed} nós**")
st.write(f"Posição: **X = {st.session_state.x} | Y = {st.session_state.y}**")

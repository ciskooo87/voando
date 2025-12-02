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
# LOAD ASSETS (MAPA + AVIÃO)
# ======================================================

# Carrega e converte para RGB
map_bg = load_image("data/tiles/map_base.png").convert("RGB")

plane_raw = load_image("assets/plane2.png").convert("RGB")

# 🔥 Redimensiona o avião para tamanho fixo controlado
PLANE_SIZE = 64
plane = plane_raw.resize((PLANE_SIZE, PLANE_SIZE))
plane_arr = np.array(plane)
pw, ph = PLANE_SIZE, PLANE_SIZE

# ======================================================
# GAME STATE (SESSION)
# ======================================================
if "x" not in st.session_state:
    st.session_state.x = 400
if "y" not in st.session_state:
    st.session_state.y = 300
if "speed" not in st.session_state:
    st.session_state.speed = 5

# ======================================================
# LAYOUT
# ======================================================
col1, col2 = st.columns([1, 4])

# ======================================================
# CONTROLES DO AVIÃO
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

    # Mapa como matriz
    canvas = np.array(map_bg).copy()

    px = int(st.session_state.x)
    py = int(st.session_state.y)

    H, W, _ = canvas.shape

    # Proteção de borda TOTAL
    px = max(0, min(px, W - pw))
    py = max(0, min(py, H - ph))

    st.session_state.x = px
    st.session_state.y = py

    # Render seguro do avião
    canvas[py:py+ph, px:px+pw] = plane_arr

    # Exibe
    st.image(canvas, use_column_width=True)

# ======================================================
# PAINEL
# ======================================================
st.markdown("---")
st.write(f"Velocidade: **{st.session_state.speed} nós**")
st.write(f"Posição: **X = {st.session_state.x} | Y = {st.session_state.y}**")

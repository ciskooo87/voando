import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(layout="wide")

# ======================================================
# LOAD ASSETS
# ======================================================
plane = Image.open("assets/plane.png")
map_bg = Image.open("data/tiles/map_base.png")

# Posição inicial
if "x" not in st.session_state:
    st.session_state.x = 400
    st.session_state.y = 300
    st.session_state.speed = 5

# ======================================================
# CONTROLES DO AVIÃO
# ======================================================
col1, col2 = st.columns([1, 4])

with col1:
    st.markdown("### Controles")
    
    if st.button("⬆️ Acelerar"):
        st.session_state.speed += 1

    if st.button("⬇️ Desacelerar"):
        st.session_state.speed = max(1, st.session_state.speed - 1)

    if st.button("⬅️ Esquerda"):
        st.session_state.x -= st.session_state.speed

    if st.button("➡️ Direita"):
        st.session_state.x += st.session_state.speed

    if st.button("⬆️ Frente"):
        st.session_state.y -= st.session_state.speed

    if st.button("⬇️ Trás"):
        st.session_state.y += st.session_state.speed

with col2:
    st.markdown("## 🛫 FlightBuilder2D – MVP")
    canvas = np.array(map_bg).copy()

    # Colocar avião no mapa
    px, py = st.session_state.x, st.session_state.y
    pw, ph = plane.size

    # Render plane
    canvas[py:py+ph, px:px+pw] = np.array(plane)

    st.image(canvas, use_column_width=True)

# Painel do avião
st.markdown("---")
st.markdown(f"**Velocidade:** {st.session_state.speed} nós")
st.markdown(f"**Posição:** X={st.session_state.x}, Y={st.session_state.y}")

"""login.py — Página de autenticación"""
import streamlit as st
import time

st.set_page_config(page_title="CapacitaSOC · Login", page_icon="🛡️", layout="centered")

st.markdown("""
<style>
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer { display:none; }
    .block-container { padding: 4rem 2rem; max-width: 420px; }
</style>
""", unsafe_allow_html=True)

st.markdown("## 🛡️ CapacitaSOC")
st.markdown("Plataforma de Entrenamiento para Analistas SOC")
st.divider()

username = st.text_input("Usuario", placeholder="analista@soc.corp")
password = st.text_input("Contraseña", type="password", placeholder="••••••••")

if st.button("Iniciar sesión", use_container_width=True, type="primary"):
    if username and password:
        with st.spinner("Verificando..."):
            time.sleep(0.8)
        st.success("Acceso concedido")
        time.sleep(0.5)
        st.switch_page("pages/1_Dashboard.py")
    else:
        st.error("Ingresa usuario y contraseña.")

st.caption("Demo: cualquier usuario y contraseña funcionan.")

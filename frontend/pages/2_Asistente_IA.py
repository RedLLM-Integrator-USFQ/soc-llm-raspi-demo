"""pages/2_Asistente_IA.py — Chat con el asistente IA"""
import streamlit as st
import time

st.set_page_config(page_title="Asistente IA — CapacitaSOC", page_icon="💬", layout="centered")

st.markdown("""
<style>
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer { display:none; }
    .block-container { padding: 2rem 2rem 1rem; max-width: 780px; }

    .chat-outer { display:flex; flex-direction:column; gap:12px;
                  max-height:520px; overflow-y:auto; padding:4px 2px 12px; }
    .bubble-wrap-user { display:flex; flex-direction:column; align-items:flex-end; }
    .bubble-wrap-ai   { display:flex; flex-direction:column; align-items:flex-start; }
    .lbl  { font-size:10px; color:#aaa; margin-bottom:3px; }
    .bubble-user { background:#1a73e8; color:#fff;
                   border-radius:16px 16px 4px 16px;
                   padding:10px 15px; max-width:75%;
                   font-size:13px; line-height:1.55; }
    .bubble-ai   { background:#f1f3f4; color:#111;
                   border-radius:16px 16px 16px 4px;
                   padding:10px 15px; max-width:75%;
                   font-size:13px; line-height:1.55; }
</style>
""", unsafe_allow_html=True)

def _mock_response(msg: str) -> str:
    m = msg.lower()
    if any(w in m for w in ["ransomware","malware","virus"]):
        return "🔴 **Alerta Crítica.** Recomiendo aislar el endpoint afectado inmediatamente y escalar al Tier 3. ¿Genero el playbook de contención?"
    if any(w in m for w in ["phishing","correo","email"]):
        return "📧 Para phishing: bloquea el remitente en el gateway, verifica si otros usuarios recibieron el mismo correo y extrae los IOCs del encabezado. ¿Quieres la plantilla de análisis?"
    if any(w in m for w in ["inc-","incidente","caso"]):
        return "📁 Puedo ayudarte a analizar ese incidente. Comparte el ID o los logs y lo reviso contigo paso a paso."
    if any(w in m for w in ["brute force","ssh","fuerza bruta"]):
        return "🔒 Brute force detectado. Verifica intentos fallidos en `/var/log/auth.log`, bloquea la IP en el firewall y considera habilitar fail2ban. ¿Te guío en el proceso?"
    return "🤖 Entendido. Estoy aquí para apoyarte en el análisis. ¿Puedes darme más contexto sobre lo que necesitas investigar?"

# Historial inicial
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "ai", "content": "👋 Hola, soy **CapacitaSOC IA**. Estoy listo para ayudarte a analizar alertas, revisar incidentes o guiarte en playbooks. ¿En qué te ayudo?"}
    ]

st.markdown("## 💬 Asistente IA — CapacitaSOC")
st.caption("Consulta sobre alertas, incidentes o procedimientos. La IA te guía en tiempo real.")
st.divider()

# Renderizar historial
bubbles = ""
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        bubbles += f'<div class="bubble-wrap-user"><div class="lbl">Tú</div><div class="bubble-user">{msg["content"]}</div></div>'
    else:
        bubbles += f'<div class="bubble-wrap-ai"><div class="lbl">CapacitaSOC IA</div><div class="bubble-ai">{msg["content"]}</div></div>'

st.markdown(f'<div class="chat-outer">{bubbles}</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Input
col_inp, col_btn = st.columns([5, 1])
with col_inp:
    user_input = st.text_input("", placeholder="Escribe tu consulta...", label_visibility="collapsed", key="chat_input")
with col_btn:
    send = st.button("Enviar", use_container_width=True, type="primary", key="chat_send")

if send and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
    with st.spinner("CapacitaSOC IA está pensando..."):
        time.sleep(0.6)
    st.session_state.chat_history.append({"role": "ai", "content": _mock_response(user_input.strip())})
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
col_sug, _ = st.columns([3, 1])
with col_sug:
    st.markdown("**Sugerencias rápidas:**")
    s1, s2, s3 = st.columns(3)
    if s1.button("🔴 Ransomware"):
        st.session_state.chat_history.append({"role": "user", "content": "Tengo un caso de ransomware, ¿qué hago?"})
        st.session_state.chat_history.append({"role": "ai", "content": _mock_response("ransomware")})
        st.rerun()
    if s2.button("📧 Phishing"):
        st.session_state.chat_history.append({"role": "user", "content": "¿Cómo analizo un correo de phishing?"})
        st.session_state.chat_history.append({"role": "ai", "content": _mock_response("phishing")})
        st.rerun()
    if s3.button("🔒 Brute Force"):
        st.session_state.chat_history.append({"role": "user", "content": "Detecté brute force en SSH"})
        st.session_state.chat_history.append({"role": "ai", "content": _mock_response("brute force")})
        st.rerun()

if len(st.session_state.chat_history) > 1:
    if st.button("🗑 Limpiar conversación"):
        st.session_state.chat_history = [st.session_state.chat_history[0]]
        st.rerun()

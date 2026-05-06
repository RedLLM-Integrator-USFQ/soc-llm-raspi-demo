"""pages/2_Asistente_IA.py — Chat con el asistente IA (conectado a FastAPI /generate)"""
import os
import time
import requests
import streamlit as st

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
    .latency-badge { font-size:10px; color:#aaa; margin-top:4px; }
</style>
""", unsafe_allow_html=True)

# ── Configuración ─────────────────────────────────────────────────────────────
API_URL   = os.getenv("API_URL", "http://api:8000")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2:1b")

SYSTEM_PROMPT = (
    "Eres CapacitaSOC IA, un asistente experto en ciberseguridad para analistas SOC. "
    "Respondes en español, de forma concisa y práctica. "
    "Cuando detectes una amenaza, indica el nivel de riesgo (Crítica/Alta/Media/Baja) "
    "y recomienda acción inmediata. "
    "Usa emojis: 🔴 crítico, 🟠 alto, 🟡 medio, 🟢 bajo. "
    "Basa tus respuestas estrictamente en el contexto de seguridad operacional."
)


def call_generate(user_msg: str) -> tuple[str, float]:
    """Llama a /generate de la FastAPI. Retorna (respuesta, latencia_seg)."""
    prompt = f"{SYSTEM_PROMPT}\n\nAnalista: {user_msg}\nCapacitaSOC IA:"
    try:
        t0 = time.time()
        resp = requests.post(
            f"{API_URL}/generate",
            json={"model": LLM_MODEL, "prompt": prompt, "stream": False},
            timeout=120,
        )
        latencia = round(time.time() - t0, 1)
        resp.raise_for_status()
        data = resp.json()
        respuesta = data.get("response", "").strip()
        if not respuesta:
            respuesta = "⚠️ El modelo no devolvió respuesta. Intenta de nuevo."
        return respuesta, latencia
    except requests.exceptions.ConnectionError:
        return "❌ No se pudo conectar con la API. ¿Está corriendo el servicio?", 0.0
    except requests.exceptions.Timeout:
        return "⏱️ Timeout: la Raspberry Pi tardó demasiado. Intenta con una pregunta más corta.", 0.0
    except Exception as e:
        return f"❌ Error inesperado: {e}", 0.0


# ── Estado inicial ────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "ai",
            "content": "👋 Hola, soy CapacitaSOC IA. Estoy listo para ayudarte a analizar alertas, revisar incidentes o guiarte en playbooks. ¿En qué te ayudo?",
            "latencia": None,
        }
    ]

st.markdown("## 💬 Asistente IA — CapacitaSOC")
st.caption("Consulta sobre alertas, incidentes o procedimientos. La IA te guía en tiempo real.")
st.markdown(
    f'<div style="font-size:11px;color:#888;margin-bottom:8px;">'
    f'🤖 Modelo: <code>{LLM_MODEL}</code> · API: <code>{API_URL}</code></div>',
    unsafe_allow_html=True,
)
st.divider()

# ── Historial ─────────────────────────────────────────────────────────────────
bubbles = ""
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        bubbles += (
            f'<div class="bubble-wrap-user">'
            f'<div class="lbl">Tú</div>'
            f'<div class="bubble-user">{msg["content"]}</div>'
            f'</div>'
        )
    else:
        lat_html = (
            f'<div class="latency-badge">⏱ {msg["latencia"]}s</div>'
            if msg.get("latencia") is not None else ""
        )
        bubbles += (
            f'<div class="bubble-wrap-ai">'
            f'<div class="lbl">CapacitaSOC IA</div>'
            f'<div class="bubble-ai">{msg["content"]}</div>'
            f'{lat_html}</div>'
        )

st.markdown(f'<div class="chat-outer">{bubbles}</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
col_inp, col_btn = st.columns([5, 1])
with col_inp:
    user_input = st.text_input(
        "", placeholder="Escribe tu consulta...",
        label_visibility="collapsed", key="chat_input",
    )
with col_btn:
    send = st.button("Enviar", use_container_width=True, type="primary", key="chat_send")


def _enviar(msg: str):
    st.session_state.chat_history.append({"role": "user", "content": msg, "latencia": None})
    with st.spinner("⏳ CapacitaSOC IA procesando en la Raspberry Pi..."):
        respuesta, latencia = call_generate(msg)
    st.session_state.chat_history.append({"role": "ai", "content": respuesta, "latencia": latencia})
    st.rerun()


if send and user_input.strip():
    _enviar(user_input.strip())

# ── Sugerencias rápidas ───────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col_sug, _ = st.columns([3, 1])
with col_sug:
    st.markdown("Sugerencias rápidas:")
    s1, s2, s3 = st.columns(3)
    if s1.button("🔴 Ransomware"):
        _enviar("Tengo un caso de ransomware, ¿qué hago?")
    if s2.button("📧 Phishing"):
        _enviar("¿Cómo analizo un correo de phishing?")
    if s3.button("🔒 Brute Force"):
        _enviar("Detecté brute force en SSH")

if len(st.session_state.chat_history) > 1:
    if st.button("🗑 Limpiar conversación"):
        st.session_state.chat_history = [st.session_state.chat_history[0]]
        st.rerun()

"""
components/chat_ai.py
─────────────────────
Componente: Asistente IA — CapacitaSOC Chat
Integración UX: panel lateral / expander dentro del dashboard.

Lógica frontend:
  - El analista escribe y envía mensajes.
  - Los mensajes aparecen en pantalla inmediatamente (sin backend IA aún).
  - Placeholder de respuesta simulada para mostrar el flujo conversacional.
  - Estructura lista para conectar a un LLM (OpenAI, Anthropic, etc.)
    reemplazando la función `_mock_response`.
"""

import streamlit as st
import time


# ── Respuesta placeholder (reemplazar por llamada real al LLM) ────────────────
def _mock_response(user_msg: str) -> str:
    """
    Stub: simula una respuesta de la IA.
    Reemplazar por:  response = llm_client.chat(user_msg)
    """
    msg = user_msg.lower()
    if any(w in msg for w in ["ransomware", "malware", "virus"]):
        return "🔴 **Alerta Crítica detectada.** Recomiendo aislar el endpoint afectado de inmediato y escalar al Tier 3. ¿Quieres que genere el playbook de contención?"
    if any(w in msg for w in ["phishing", "correo", "email"]):
        return "📧 Para incidentes de phishing: bloquea el remitente en el gateway, revisa si otros usuarios recibieron el mismo correo y extrae los IOCs del encabezado. ¿Necesitas la plantilla de análisis?"
    if any(w in msg for w in ["inc-", "incidente", "caso"]):
        return "📁 Puedo ayudarte a analizar ese incidente. Comparte el ID o los logs relevantes y lo reviso contigo paso a paso."
    return "🤖 Entendido. Estoy aquí para apoyarte en el análisis. ¿Puedes darme más contexto sobre lo que necesitas investigar?"


# ── Render principal ──────────────────────────────────────────────────────────
def render_chat() -> None:
    """Renderiza el componente de chat del asistente IA."""

    # Inicializar historial en session_state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "ai",
                "content": "👋 Hola, soy **CapacitaSOC IA**. Estoy listo para ayudarte a analizar alertas, revisar incidentes o guiarte en el playbook. ¿En qué te ayudo?",
            }
        ]

    st.markdown("""
    <style>
    .chat-wrap {
        display:flex; flex-direction:column; gap:10px;
        max-height:380px; overflow-y:auto; padding:4px 2px 8px;
    }
    .msg-user {
        align-self:flex-end; background:#1a73e8; color:#fff;
        border-radius:16px 16px 4px 16px; padding:9px 14px;
        max-width:80%; font-size:13px; line-height:1.5;
    }
    .msg-ai {
        align-self:flex-start; background:#f1f3f4; color:#111;
        border-radius:16px 16px 16px 4px; padding:9px 14px;
        max-width:80%; font-size:13px; line-height:1.5;
    }
    .msg-lbl { font-size:10px; color:#aaa; margin-bottom:2px; }
    </style>
    """, unsafe_allow_html=True)

    # Renderizar historial
    chat_html = '<div class="chat-wrap">'
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            chat_html += f'<div class="msg-lbl" style="text-align:right">Tú</div><div class="msg-user">{msg["content"]}</div>'
        else:
            chat_html += f'<div class="msg-lbl">CapacitaSOC IA</div><div class="msg-ai">{msg["content"]}</div>'
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Input + envío
    col_inp, col_btn = st.columns([5, 1])
    with col_inp:
        user_input = st.text_input(
            label="",
            placeholder="Escribe tu consulta al analista IA...",
            key="chat_input",
            label_visibility="collapsed",
        )
    with col_btn:
        send = st.button("Enviar", use_container_width=True, key="chat_send")

    if send and user_input.strip():
        # Agregar mensaje del usuario
        st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})

        # Simular respuesta IA (reemplazar por llamada real)
        with st.spinner("CapacitaSOC IA está pensando..."):
            time.sleep(0.6)
        response = _mock_response(user_input.strip())
        st.session_state.chat_history.append({"role": "ai", "content": response})

        st.rerun()

    # Botón limpiar historial
    if len(st.session_state.chat_history) > 1:
        if st.button("🗑 Limpiar conversación", key="chat_clear"):
            st.session_state.chat_history = [st.session_state.chat_history[0]]
            st.rerun()

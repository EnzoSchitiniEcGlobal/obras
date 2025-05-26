import streamlit as st
import requests
import uuid

st.set_page_config(page_title="🤖 Chat com o labFlix", page_icon="💬", layout="centered")

# Inicializa sessão e mensagens
if "mensagens" not in st.session_state:
    st.session_state["mensagens"] = []

if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4().hex)

# Função para enviar mensagem ao webhook n8n
def enviar_para_n8n(chat_input, session_id):
    webhook_url = "https://n8n.wokpy.io/webhook/1eac00e8-695e-4254-bb7d-826bcb294edf/chat"
    payload = {
        "sessionId": session_id,
        "action": "sendMessage",
        "chatInput": chat_input
    }
    try:
        response = requests.post(webhook_url, data=payload)
        response.raise_for_status()
        return response.json().get("output", "⚠️ Resposta vazia.")
    except Exception as e:
        return f"❌ Erro: {e}"

# Caixa de input na parte inferior
mensagem = st.chat_input("Digite sua mensagem...")

# Se mensagem foi enviada, adiciona antes de renderizar
if mensagem:
    st.session_state["mensagens"].append(("Você", mensagem))
    resposta = enviar_para_n8n(mensagem, st.session_state["session_id"])
    st.session_state["mensagens"].append(("Assistente", resposta))

# Exibe mensagens (ordem natural: antigas em cima, novas embaixo)
st.title("💬 Chat com o labFlix")
chat_container = st.container()

with chat_container:
    for remetente, texto in st.session_state["mensagens"]:
        with st.chat_message("user" if remetente == "Você" else "assistant"):
            st.markdown(texto)

    # âncora para rolar até o fim
    st.markdown("<div id='fim'></div>", unsafe_allow_html=True)
    st.markdown(
        """<script>
        const chatEnd = document.getElementById('fim');
        if (chatEnd) {
            chatEnd.scrollIntoView({ behavior: 'smooth' });
        }
        </script>""",
        unsafe_allow_html=True,
    )

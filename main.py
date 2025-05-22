# app.py

import streamlit as st
from airtable import get_transcriptions
from memory_faiss import create_index, search_index
from gemini import ask_gemini

# Configurações iniciais da página
st.set_page_config(page_title="Chatbot de Reuniões", layout="centered")
st.title("🤖 Chatbot de Reuniões com Memória Expandida")

# Inicialização (cache para não carregar sempre)
@st.cache_resource
def init():
    transcricoes = get_transcriptions(limit=10)
    create_index(transcricoes)
    return transcricoes

transcriptions = init()

# Interface
with st.form("chat_form"):
    question = st.text_input("Digite sua pergunta:")
    submitted = st.form_submit_button("Perguntar")

if submitted and question.strip():
    with st.spinner("Consultando a IA..."):
        trechos_relevantes = search_index(question, transcriptions)
        contexto = "\n\n".join(trechos_relevantes)
        resposta = ask_gemini(contexto, question)
        st.markdown("### 💬 Resposta")
        st.write(resposta)

        with st.expander("🧠 Contexto utilizado"):
            st.code(contexto)

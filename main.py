import streamlit as st
from airtable import get_transcriptions
from memory_faiss import create_index, search_index
from gemini import ask_gemini

# Inicializar sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Título
st.title("🤖 Chatbot Gemini com Memória")

# Carregar transcrições e criar índice
transcriptions = get_transcriptions(limit=10)
create_index(transcriptions)

# Mostrar histórico do chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada do usuário
if prompt := st.chat_input("Digite sua pergunta sobre as reuniões..."):
    # Mostrar pergunta do usuário
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Buscar documentos relevantes e gerar resposta
    relevant_docs = search_index(prompt, transcriptions)
    context = "\n\n".join(relevant_docs)
    response = ask_gemini(context, prompt)

    # Mostrar resposta do bot
    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

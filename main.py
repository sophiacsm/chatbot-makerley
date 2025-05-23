import streamlit as st
import json
import os
from memory_faiss import create_index, search_index
from gemini import ask_gemini
from sentence_transformers import SentenceTransformer

MEMORY_FILE = "data/memory_store.json"
INDEX_PATH = "data/index.faiss"
MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# Utilitários de memória

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def update_index_from_memory(memory):
    texts = [item["user"] for item in memory]
    if texts:
        create_index(texts)

# Inicializar sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Título
st.title("🤖 Chatbot Gemini com Memória")

# Carregar memória
memory = load_memory()
update_index_from_memory(memory)

# Mostrar histórico do chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada do usuário
if prompt := st.chat_input("Digite sua pergunta..."):
    # Mostrar pergunta do usuário
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Buscar contexto relevante da memória
    relevant = search_index(prompt, [m["user"] for m in memory])
    context_pairs = [m for m in memory if m["user"] in relevant]
    context = "\n".join([f"Usuário: {m['user']}\nBot: {m['bot']}" for m in context_pairs])

    # Enviar para o Gemini com contexto
    response = ask_gemini(context, prompt)

    # Mostrar resposta e salvar na memória
    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

    memory.append({"user": prompt, "bot": response})
    save_memory(memory)
    update_index_from_memory(memory)

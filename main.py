import streamlit as st
import json
import os
from memory_faiss import create_index, search_index
from gemini import ask_gemini
from airtable import get_transcriptions
from sentence_transformers import SentenceTransformer
from get_next_event import get_next_events

MEMORY_FILE = "data/memory_store.json"
INDEX_PATH = "data/index.faiss"
MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def is_calendar_query(prompt: str) -> bool:
    keywords = [
        "próxima reunião", "quando é minha próxima reunião",
        "qual minha próxima reunião", "qual o próximo evento",
        "me dê as próximas reuniões", "eventos futuros", "reuniões futuras"
    ]
    return any(kw.lower() in prompt.lower() for kw in keywords)

# Utilitários de memória
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def update_index(transcriptions, memory):
    texts = transcriptions + [item["user"] for item in memory]
    if texts:
        create_index(texts)

# Inicializar sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Título
st.set_page_config(page_title="Chatbot de Reuniões", layout="centered")
st.title("🤖 Chatbot Gemini com Memória + Reuniões (Airtable)")

# Carregar dados
memory = load_memory()
transcriptions = get_transcriptions(limit=10)
update_index(transcriptions, memory)

# Mostrar histórico do chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada do usuário
if prompt := st.chat_input("Digite sua pergunta..."):
    # Mostrar pergunta do usuário
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Buscar contexto relevante na memória + transcrições
    memory_texts = [m["user"] for m in memory]
    all_texts = transcriptions + memory_texts
    relevant = search_index(prompt, all_texts)

    context_from_transcriptions = [t for t in transcriptions if t in relevant]
    context_from_memory = [m for m in memory if m["user"] in relevant]

    context = "\n".join(
        [f"🧠 Transcrição: {t}" for t in context_from_transcriptions] +
        [f"🗣️ Usuário: {m['user']}\n🤖 Bot: {m['bot']}" for m in context_from_memory]
    )

    # Obter resposta
    if is_calendar_query(prompt):
        response = get_next_events(n=7)
    else:
        response = ask_gemini(context, prompt)

    # Mostrar resposta e salvar na memória
    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

    memory.append({"user": prompt, "bot": response})
    save_memory(memory)
    update_index(transcriptions, memory)

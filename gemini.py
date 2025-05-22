import google.generativeai as genai
import os
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

api_key = st.secrets["gemini"]["api_key"] if "gemini" in st.secrets else os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

def ask_gemini(context, question):
    prompt = f"""
Você é um assistente de reuniões. Abaixo está o contexto das últimas reuniões:

{context}

Pergunta: {question}
"""
    response = model.generate_content(prompt)
    return response.text

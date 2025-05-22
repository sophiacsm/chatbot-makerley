import google.generativeai as genai
import os
from dotenv import load_dotenv
import tomllib
load_dotenv()

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

genai.configure(api_key=config["gemini"]["api_key"])
model = genai.GenerativeModel('gemini-2.0-flash')

def ask_gemini(context, question):
    prompt = f"""
Você é um assistente de reuniões. Abaixo está o contexto das últimas reuniões:

{context}

Pergunta: {question}
"""
    response = model.generate_content(prompt)
    return response.text

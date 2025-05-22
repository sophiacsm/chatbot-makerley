import requests, os
from dotenv import load_dotenv
import tomllib
import streamlit as st
load_dotenv()

API_KEY = st.secrets["airtable"]["api_key"] if "airtable" in st.secrets else os.getenv("API_KEY")
BASE_ID = st.secrets["airtable"]["base_id"] if "airtable" in st.secrets else os.getenv("BASE_ID")
TABLE_NAME = st.secrets["airtable"]["table_name"] if "airtable" in st.secrets else os.getenv("TABLE_NAME")

HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

def get_transcriptions(limit=10):
    url = f'https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}?sort[0][field]=Data&sort[0][direction]=desc&maxRecords={limit}'
    r = requests.get(url, headers=HEADERS).json()
    registros = r.get('records', [])

    docs = []
    for rec in registros:
        fields = rec.get("fields", {})
        titulo = fields.get("Título", "Sem título")
        texto = fields.get("Texto", "")
        data = fields.get("Data", "Sem data")

        full_text = f"📅 {data}\n📝 {titulo}\n{texto}"
        docs.append(full_text)

    return docs

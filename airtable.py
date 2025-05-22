import requests, os
from dotenv import load_dotenv
import tomllib
load_dotenv()

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

API_KEY = config["airtable"]["api_key"]
BASE_ID = config["airtable"]["base_id"]
TABLE_NAME = config["airtable"]["table_name"]

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

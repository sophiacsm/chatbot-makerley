import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
import pytz

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_next_events(n=7):
    # Lê as credenciais diretamente dos secrets
    creds_dict = {
        "client_id": st.secrets["google"]["client_id"],
        "client_secret": st.secrets["google"]["client_secret"],
        "refresh_token": st.secrets["google"]["refresh_token"],
        "token_uri": st.secrets["google"]["token_uri"]
    }

    creds = Credentials.from_authorized_user_info(info=creds_dict, scopes=SCOPES)

    service = build('calendar', 'v3', credentials=creds)
    now = datetime.utcnow().isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=n,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    response_lines = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary = event.get('summary', 'Sem título')
        attendees = event.get('attendees', [])
        people = ', '.join([a['email'] for a in attendees]) if attendees else 'Sem participantes'
        response_lines.append(f"📅 {summary} — {start}\n👥 Participantes: {people}")

    return "\n\n".join(response_lines) if response_lines else "Você não tem eventos futuros."

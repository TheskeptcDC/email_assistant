import os
import base64
import re
from datetime import datetime, timedelta
from email import message_from_bytes
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import requests

# Gmail scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SUMMARY_API_URL = "http://127.0.0.1:8000/summarize"

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def clean_text(text):
    text = re.sub(r'https?://\S+', '', text)  # Remove URLs
    text = re.sub(r'(?i)(unsubscribe|privacy policy|terms of service|view in browser|click here).*', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def get_todays_emails(service):
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    after = int(today.timestamp())
    
    response = service.users().messages().list(
        userId='me',
        q=f'after:{after}',
        maxResults=50  # Adjust as needed
    ).execute()

    messages = response.get('messages', [])
    if not messages:
        return ["No messages found today."]

    email_texts = []

    for msg in messages:
        msg_detail = service.users().messages().get(userId='me', id=msg['id'], format='raw').execute()
        raw_msg = base64.urlsafe_b64decode(msg_detail['raw'].encode('ASCII'))
        mime_msg = message_from_bytes(raw_msg)

        subject = mime_msg.get('Subject', 'No Subject')
        sender = mime_msg.get('From', 'Unknown Sender')

        body = ""
        if mime_msg.is_multipart():
            for part in mime_msg.walk():
                if part.get_content_type() == "text/plain":
                    charset = part.get_content_charset() or "utf-8"
                    body = part.get_payload(decode=True).decode(charset, errors="replace")
                    break
        else:
            body = mime_msg.get_payload(decode=True).decode(mime_msg.get_content_charset() or "utf-8", errors="replace")

        clean_body = clean_text(body)
        email_entry = f"From: {sender}\nSubject: {subject}\n\n{clean_body}"
        email_texts.append(email_entry)

    return email_texts

def summarize_content(email_text):
    payload = {
        "content": email_text,
        "model": "llama3.2"
    }
    response = requests.post(SUMMARY_API_URL, json=payload)
    return response.json().get("response", "No summary generated.")

if __name__ == '__main__':
    service = get_gmail_service()
    emails = get_todays_emails(service)

    combined_content = "\n\n---\n\n".join(emails)
    print("📩 COMBINED EMAIL CONTENT:\n", combined_content)

    print("\n🔍 SUMMARIZING TODAY'S EMAILS...")
    summary = summarize_content(combined_content)
    print("\n🧠 SUMMARY:\n", summary)

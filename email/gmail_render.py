import os
import base64
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email import message_from_bytes

# If modifying scopes, delete token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

def get_latest_email(service):
    results = service.users().messages().list(userId='me', maxResults=1).execute()
    messages = results.get('messages', [])
    if not messages:
        return "No messages found."

    msg_id = messages[0]['id']
    msg = service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
    raw_msg = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
    mime_msg = message_from_bytes(raw_msg)
    return mime_msg.get_payload()

if __name__ == '__main__':
    service = get_gmail_service()
    email_content = get_latest_email(service)
    print("📩 Latest Email Content:\n", email_content)

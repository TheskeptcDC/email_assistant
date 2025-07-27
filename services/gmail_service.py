import os
import base64
from email import message_from_bytes
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

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
    return build('gmail', 'v1', credentials=creds)

def fetch_today_emails(service, max_results=10):
    from datetime import datetime
    import time

    today = datetime.now().strftime('%Y/%m/%d')
    query = f"after:{today}"
    results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
    return results.get('messages', [])
    
# def get_email_content(service, msg_id):
#     msg = service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
#     raw_msg = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
#     mime_msg = message_from_bytes(raw_msg)

#     subject = mime_msg.get('Subject', 'No Subject')
#     sender = mime_msg.get('From', 'Unknown Sender')

#     body = ""
#     if mime_msg.is_multipart():
#         for part in mime_msg.walk():
#             if part.get_content_type() == "text/plain":
#                 charset = part.get_content_charset() or "utf-8"
#                 body = part.get_payload(decode=True).decode(charset, errors="replace")
#                 break
#     else:
#         body = mime_msg.get_payload(decode=True).decode(mime_msg.get_content_charset() or "utf-8", errors="replace")

#     return sender, subject, body

def get_email_content(service, msg_id):
    try:
        msg = service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
        raw_msg = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
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

        return sender, subject, body

    except HttpError as e:
        return "Error fetching email content: " + str(e)
    except Exception as e:
        return "Unexpected error: " + str(e)

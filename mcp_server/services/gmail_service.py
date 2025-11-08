# # mcp_server/services/gmail_service.py
# import base64
# from googleapiclient.discovery import build
# from .calendar_service import mark_message_read

# def get_unread_emails(creds, max_results=2):
#     service = build('gmail', 'v1', credentials=creds)
#     results = service.users().messages().list(
#         userId='me',
#         labelIds=['INBOX'],
#         q='is:unread',
#         maxResults=max_results
#     ).execute()

#     messages = results.get('messages', [])
#     emails = []

#     for msg in messages:
#         msg_id = msg['id']
#         try:
#             msg_data = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
#             payload = msg_data.get('payload', {})
#             headers = payload.get('headers', [])
#             subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
#             sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')

#             # Decode plain text or HTML body
#             body = ""
#             parts = payload.get('parts', [])
#             if parts:
#                 for part in parts:
#                     data = part.get('body', {}).get('data')
#                     if data:
#                         body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
#                         break

#             emails.append({
#                 "id": msg_id,
#                 "from": sender,
#                 "subject": subject,
#                 "body": body[:2000]
#             })

#             # Mark as read
#             mark_message_read(service, msg_id)

#         except Exception as e:
#             print(f"⚠️ Error reading message {msg_id}: {e}")
#             continue

#     return emails

# mcp_server/services/gmail_service.py
import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from mcp_server.utils.auth_loader import load_credentials
from utils.logger import inbox, success, warn, error

def fetch_emails(creds=None, max_results=2):
    """
    Fetch unread Gmail emails using Google API.
    """
    try:
        if creds is None:
            creds = load_credentials()

        service = build('gmail', 'v1', credentials=creds)
        inbox("📨 Fetching unread emails...")

        results = service.users().messages().list(
            userId='me',
            labelIds=['INBOX'],
            q='is:unread',
            maxResults=max_results
        ).execute()

        messages = results.get('messages', [])
        if not messages:
            warn("No unread messages found.")
            return []

        emails = []
        for msg in messages:
            msg_id = msg['id']
            msg_data = service.users().messages().get(
                userId='me', id=msg_id, format='full'
            ).execute()

            payload = msg_data.get('payload', {})
            headers = payload.get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')

            # Decode body
            body = ""
            parts = payload.get('parts', [])
            if parts:
                for part in parts:
                    data = part.get('body', {}).get('data')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                        break
            else:
                data = payload.get('body', {}).get('data')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

            emails.append({
                "id": msg_id,
                "from": sender,
                "subject": subject,
                "body": body[:2000]
            })

            # Mark as read
            try:
                service.users().messages().modify(
                    userId='me',
                    id=msg_id,
                    body={'removeLabelIds': ['UNREAD']}
                ).execute()
                success(f"📬 Marked as read: {subject}")
            except Exception as mark_err:
                warn(f"⚠️ Could not mark {msg_id} as read: {mark_err}")

        success(f"✅ Returning {len(emails)} emails")
        return emails

    except Exception as e:
        error(f"❌ Exception in fetch_emails: {e}")
        return []

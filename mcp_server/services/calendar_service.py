# mcp_server/services/calendar_service.py
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone

def mark_message_read(service, msg_id):
    try:
        service.users().messages().modify(
            userId='me',
            id=msg_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
    except Exception as e:
        print(f"⚠️ Could not mark message {msg_id} as read: {e}")

def create_calendar_event(creds, data):
    service = build('calendar', 'v3', credentials=creds)
    tz = "Asia/Kolkata"

    start_iso = data.get("start_iso")
    duration = int(data.get("duration_minutes", 30))

    start_dt = (
        datetime.fromisoformat(start_iso)
        if start_iso else
        datetime.now(tz=timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=10)
    )

    end_dt = start_dt + timedelta(minutes=duration)

    event = {
        "summary": data.get("summary", "Reminder from FastAgent"),
        "description": data.get("description", ""),
        "start": {"dateTime": start_dt.isoformat(), "timeZone": tz},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": tz},
    }

    created = service.events().insert(calendarId='primary', body=event).execute()
    return {
        "status": "created",
        "event_id": created.get("id"),
        "start": created.get("start", {})
    }

from datetime import datetime
from app.gmail_auth import get_gmail_services
import base64
import re


def mark_email_as_read(message_id):

    service = get_gmail_services()

    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={
            "removeLabelIds": ["UNREAD"]
        }
    ).execute()

def decode_base64(data):
    return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")


def clean_html(html):
    # remove scripts/styles
    html = re.sub(r"<(script|style).*?>.*?</\1>", "", html, flags=re.DOTALL)

    # remove all tags
    text = re.sub(r"<.*?>", " ", html)

    # remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_body(payload):
    """
    Recursively search Gmail MIME parts
    """

    body = ""

    # If body exists directly
    if payload.get("body", {}).get("data"):
        return decode_base64(payload["body"]["data"])

    # Search in parts
    parts = payload.get("parts", [])

    for part in parts:

        mime_type = part.get("mimeType")

        # Prefer plain text
        if mime_type == "text/plain":
            data = part["body"].get("data")
            if data:
                return decode_base64(data)

        # Fallback HTML
        if mime_type == "text/html":
            data = part["body"].get("data")
            if data:
                html = decode_base64(data)
                return clean_html(html)

        # Recursive search (important for Gmail nested MIME)
        if "parts" in part:
            nested = extract_body(part)
            if nested:
                return nested

    return body


def fetch_unread_emails():

    service = get_gmail_services()

    query = "is:unread newer_than:3d"

    results = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=10
    ).execute()

    messages = results.get("messages", [])

    emails = []

    for message in messages:

        msg = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="full"
        ).execute()

        payload = msg["payload"]
        headers = payload["headers"]

        subject = ""
        sender = ""
        date = ""

        for header in headers:

            if header["name"] == "Subject":
                subject = header["value"]

            elif header["name"] == "From":
                sender = header["value"]

            elif header["name"] == "Date":
                date = header["value"]

        body = extract_body(payload)

        # optional: reduce size before LLM
        body = body[:2000]

        emails.append({
            "id": message["id"],
            "subject": subject,
            "sender": sender,
            "body": body,
            "date": date
        })

    return emails
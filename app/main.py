import json
import re
from datetime import datetime

from app.email_reader import fetch_unread_emails, mark_email_as_read, has_unread_emails
from app.job_extractor import extract_job_info
from app.telegram_sender import send_job_alert, send_summary


def extract_json(text):
    """
    Extract valid JSON from LLM response
    """
    text = re.sub(r"```json|```", "", text).strip()

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return json.loads(match.group())

    return None



def run():

    now = datetime.now().hour

    if now < 6:
        return
    
    if not has_unread_emails():
        return

    emails = fetch_unread_emails()

    for email in emails:

        subject = email["subject"]
        body = email["body"]


        # Skip tiny emails (notifications / footers)
        if len(body.strip()) < 50:
            continue

        # limit size to save tokens
        body = body[:2000]

        # Ask LLM to analyze email
        response = extract_job_info(body)
        job = extract_json(response)

        if not job:
            continue

        email_type = job.get("type", "").upper()

        # ---------- JOB EMAIL ----------
        if email_type == "JOB":
            send_job_alert(job, email["date"])
            mark_email_as_read(email["id"])

        # ---------- AI RELATED ----------
        elif email_type == "AI_RELATED":
            send_summary(job["summary"], email)
            mark_email_as_read(email["id"])

        # ---------- IGNORE ----------
        else:
            continue


if __name__ == "__main__":
    run()

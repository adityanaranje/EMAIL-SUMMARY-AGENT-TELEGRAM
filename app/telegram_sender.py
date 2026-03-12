import requests
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def is_valid_url(url):
    if not url:
        return False
    return url.startswith("http")


def send_job_alert(job, email_time):

    skills = "\n".join([f"    • {s}" for s in job.get("skills", [])])
    summary = "\n".join([f"    • {s}" for s in job.get("summary", [])])

    message = f"""
    🚨 {job.get('role','')} - {job.get('company','')}

    📍 Location: {job.get('location','')}
    💼 Experience: {job.get('experience','')}
    ⏰ Email Time: {email_time}

    🛠 Skills
    {skills}

    🧠 Summary
    {summary}
    """

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    buttons = []

    if is_valid_url(job.get("apply_link")):
        buttons.append({"text": "Apply Now", "url": job["apply_link"]})

    if is_valid_url(job.get("company_link")):
        buttons.append({"text": "View Company", "url": job["company_link"]})

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    if buttons:
        payload["reply_markup"] = {
            "inline_keyboard": [buttons]
        }


    requests.post(url, json=payload)

def send_summary(summary, email):

    summary_text = "\n".join([f"• {s}" for s in summary])

    message = f"""
    📧 AI Related Email

    📌 Subject: {email['subject']}
    ⏰ Email Time: {email['date']}

    🧠 Summary
    {summary_text}
    """

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    requests.post(url, json=payload)
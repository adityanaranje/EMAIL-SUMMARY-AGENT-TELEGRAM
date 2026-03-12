import os
import json

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def get_gmail_services():

    creds = None

    # ---------- 1️⃣ Load token from GitHub ENV ----------
    token_json = os.getenv("GMAIL_TOKEN")

    if token_json:
        creds = Credentials.from_authorized_user_info(
            json.loads(token_json),
            SCOPES
        )

    # ---------- 2️⃣ Local development ----------
    elif os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    # ---------- 3️⃣ Refresh token if expired ----------
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    # ---------- 4️⃣ Only allow OAuth login locally ----------
    if not creds or not creds.valid:

        # If running in GitHub Actions → stop
        if os.getenv("GITHUB_ACTIONS"):
            raise RuntimeError(
                "GMAIL_TOKEN missing or invalid in GitHub Actions"
            )

        creds_json = os.getenv("GMAIL_CREDENTIALS")

        if creds_json:
            client_config = json.loads(creds_json)

            flow = InstalledAppFlow.from_client_config(
                client_config,
                SCOPES
            )

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

        creds = flow.run_local_server(port=0)

        # Save token locally
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    return service
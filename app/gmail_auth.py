import os
import json

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def get_gmail_services():

    creds = None

    # Read token from ENV
    token_json = os.getenv("GMAIL_TOKEN")

    if token_json:
        creds = Credentials.from_authorized_user_info(
            json.loads(token_json),
            SCOPES
        )

    # If running locally and token file exists
    elif os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    # If token missing → create via OAuth flow
    if not creds or not creds.valid:

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

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    return service

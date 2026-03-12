from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def get_gmail_services():

    creds = None

    # Load existing token
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If token doesn't exist or expired → login
    if not creds or not creds.valid:

        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )

        creds = flow.run_local_server(port=0)

        # Save token
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)

    return service

import os
import base64
from email.message import EmailMessage
import os.path
import string

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def gmail_send_message(emailTo, emailFrom, subject="", body=""):
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id
    """

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        printable = set(string.printable)
        body = ''.join(filter(lambda x: x in printable, body))
        
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()

        message["To"] = emailTo
        message["From"] = emailFrom
        message["Subject"] = subject
        
        message.add_header('Content-Type','text/html')
        message.set_payload(body)

        # encoded message
        # print(message)
        
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        
        # pylint: disable=E1101
        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
        print(f'Message Id: {send_message["id"]}')
    
    except HttpError as error:
        print(f"An error occurred: {error}")
        send_message = None
        return send_message

from EmailedOTPHandler import EmailProviderHandler

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CLIENT_SECRETS_FILE = 'gmail_credentials.json'
TOKEN_FILE = 'token.json'


class GmailHandler(EmailProviderHandler):
    def __init__(self):
        self.service = None
        self.email_subject = None
        self.email_id = None

    def start(self, email_subject):
        self.email_subject = email_subject
        self.start_service()
        self.email_id = self.get_email_id()

    def start_service(self):  # Call the Gmail API
        try:
            self.service = build('gmail', 'v1', credentials=self.get_credentials())
        except HttpError as error:
            print(f'Gmail service start error: {error}')

    def get_credentials(self):
        creds = None
        # TOKEN_FILE stores the user's access and refresh tokens
        # it's created automatically for the first authorization
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        return creds

    def get_email_id(self):  # get the id of the last email with email_subject
        messages_list = []
        try:
            response = self.service.users().messages() \
                .list(userId='me', q=self.email_subject) \
                .execute()
            messages_list = response.get('messages', [])
        except HttpError as error:
            print(f'Gmail get email id error: {error}')
        return messages_list[0]['id'] if len(messages_list) > 0 else None

    def get_message(self):  # get the message of the email with id = email_id
        message = None
        try:
            message = self.service.users().messages().get(userId='me', id=self.email_id).execute()
        except HttpError as error:
            print(f'Gmail get message error: {error}')
        return message.get('snippet', []) if message is not None else None

    def is_email_received(self):  # check if a new email with email_subject was received
        new_email_id = self.get_email_id()
        if new_email_id is None:  # no email received
            return False
        else:
            if new_email_id == self.email_id:  # the last email is still the same
                return False
            else:  # new email received
                self.email_id = new_email_id
                return True

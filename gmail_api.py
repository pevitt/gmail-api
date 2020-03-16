from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailApi():
    
    def __init__(self):
        self.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                self.flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = self.flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=self.creds)
    
    def get_labels():
        result = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        return labels

    def get_emails(labelId):
        result = service.users().messages().list(userId='me',labelIds=[labelId]).execute()
        emails = result.get('emails', [])
        return emails

    def get_email_item(emailId):
        result = service.users().messages().get(userId='me',id=emailId).execute()
        email = result.get('emails', [])
        return email
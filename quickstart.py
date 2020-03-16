from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pprint
import sys
import os
import base64

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://mail.google.com/','https://www.googleapis.com/auth/gmail.modify']

class GmailApi():
    creds = None
    flow = None
    service = None

    def __init__(self):
        # self.creds = None
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
                pickle.dump(self.creds, token)

        self.service = build('gmail', 'v1', credentials=self.creds)
    
    def get_labels(self):
        result = self.service.users().labels().list(userId='me').execute()
        labels = result.get('labels', [])
        return labels

    def get_emails(self, labelId):
        q_string = "to:(pruebadocs@backstartup.com)"
        result = self.service.users().messages().list(userId='me',labelIds=[labelId],q=q_string).execute()
        emails = result.get('messages', [])
        return emails

    def get_email_item(self, emailId):
        result = self.service.users().messages().get(userId='me',id=emailId).execute()
        return result

    def get_email_attachments(self, messageId, attachmentId):
        result = self.service.users().messages().attachments().get(userId='me',messageId=messageId,id=attachmentId).execute()
        return result

    def set_email_read(self, messageId):
        msg_labels = {'removeLabelIds': ['UNREAD'], 'addLabelIds': ['']}
        message = self.service.users().messages().modify(userId='me', id=messageId,body=msg_labels).execute()
        return message

def main():
    test = GmailApi()
    pp = pprint.PrettyPrinter(indent=4)
    labels = test.get_labels()
    print("Labels:", labels)

    # emails = test.get_emails("UNREAD")
    # print("Emails:", emails)

    # email = test.get_email_item("168c0db33f4f7682")
    # # print("Email Body:", email)
    # pp.pprint(email)

    # for item in email['payload']['headers']:
    #     if item['name'] == 'From':
    #         email_from = item['value']
    #         email_from = email_from.split("<")
    #         print("Email From:", email_from[1].replace('>',''))

    # modify_email = test.set_email_read("168be1c4da46a7aa")
    # pp.pprint(modify_email)

    # attachment = test.get_email_attachments("168be1c4da46a7aa","ANGjdJ_aqwIwAyjS8GQCEidAy-ct4cZ6cpDtq5pu3GqadISk3tBh7axgIEePX1C993lexp1DYY1-XUKqoZbkYD4a1OaP0wV1g4KnPcZNF_-DBaKyylWoVAygZ5iy594AHJ6xb4GCXM45GpsIEWSh0YCfywSJncuSelQGSu4dg4q5tvp-h4hahq6HBE2Gg5L237sxOpP9pvog8VQUat-VRs1I-Ua2LVOztmNDKqtFWQ")
    # pp.pprint(attachment)

    
    # for part in email['payload']['parts']:
    #     if part['filename']:

    #         attachment = test.get_email_attachments("168be1c4da46a7aa",part['body']['attachmentId'])
           

    #         path = 'download/'

    #         try:
    #             os.makedirs(path)
    #         except OSError:
    #             if not os.path.isdir(path):
    #                 raise

    #         fileNamePath = os.path.join(path, part['filename'])
    #         my_file = open(fileNamePath, 'w+b')
            

    #         my_file.write(base64.urlsafe_b64decode(attachment['data']))
    #         my_file.close()

    


if __name__ == '__main__':
    main()
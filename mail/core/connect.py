import smtplib
from email.mime.text import MIMEText
import pickle
import os.path
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from googleapiclient.errors import HttpError

class GMailConnect():
    def __init__(self):
        
        """
        Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        self.creds = None

        self._login()
        self.service = build('gmail', 'v1', credentials=self.creds)


    
    def test(self):
        # For testing, read all labels in the mail account
        results = self.service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
        else:
            print('Labels:')
            for label in labels:
                print(label['name'])

    def _login(self):
        """
        Set self.creds
        """
        SCOPES = ['https://www.googleapis.com/auth/gmail.send']

        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.

        # Check if the crudential is already stored as pickle
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)
    
    def _create_msg(self, sender, to, subject, msg_txt):
        message = MIMEText(msg_txt, _charset = 'utf-8')
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        return {'raw': base64.urlsafe_b64encode(message.as_string().encode('utf-8')).decode()}

    def _send_msg(self, message, user_id="me"):
        try:
            message = (self.service.users().messages().send(userId=user_id, body=message).execute())
            print ("Message Id: %s" % message['id'])
            return message
        except HttpError as error:
            print('An error occurred: %s' % error)

def main():
    sess = GMailConnect()
    #sess.test()
    msg = sess._create_msg("me", "malloc099@gmail.com", "Hello", "This is an awesome mail.")
    sess._send_msg(msg)


if __name__ == "__main__":
    main()
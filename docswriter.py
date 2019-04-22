from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
class DocsWriter():
    def __init__(self):
        '''
        Authenticates the DocsWriter.
        '''
        self.SCOPES = ['https://www.googleapis.com/auth/documents']
        self.DOCUMENT_ID = '1dRZAWl_b9RqvrvIRM5q5XxtE5NcmeopazRk23qJshzk'

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('docs', 'v1', credentials=creds)
        self.requests = []

    def replace_text(self, old_text, new_text, case_sensitive = 'false'):
        '''
        This function appends a replace text request to the list of reqests.
        
        old_text - Text that will be replaced.
        new_text - Text that is replacing.
        case_sensitive - Either 'true' or 'false'. old_text will be checked as case sensitive or not.
        '''

        if case_sensitive != 'true' and case_sensitive != 'false':
            return

        self.requests.append(
            {
                'replaceAllText': {
                    'containsText': {
                        'text': old_text,
                        'matchCase': case_sensitive
                    },
                    'replaceText': new_text
                }
            }
        )

    def update_file(self):
        '''
        This function updates the file that is being worked with.
        '''
        result = self.service.documents().batchUpdate(documentId=self.DOCUMENT_ID, body={'requests': self.requests}).execute()

    def get_terms(self):
        '''
        This function returns the terms in the left hand column of a table.
        '''

        terms = []
        document = self.service.documents().get(documentId=self.DOCUMENT_ID).execute()

        for row in document.get('body').get('content')[2].get('table').get('tableRows'):
            term = row.get('tableCells')[0].get('content')[0].get('paragraph').get('elements')[0].get('textRun').get('content')
            term = term.strip()
            term = term.lower()
            terms.append(term)

        return terms
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class DocsWriter():
    def __init__(self, doc_id):
        '''
        Authenticates the DocsWriter.
        
        doc_id - The google docs id of the document that is being edited.
        '''
        self.SCOPES = ['https://www.googleapis.com/auth/documents']
        self.DOCUMENT_ID = doc_id

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
        Default value is 'false'
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
        self.requests = []

    def get_terms(self, lowercase = True):
        '''
        This function returns the terms in the left hand column of a table.

        lowercase - If true: returns the terms in all lowercase.
        Default value is true. 
        '''

        terms = []
        document = self.service.documents().get(documentId=self.DOCUMENT_ID).execute()

        for row in document.get('body').get('content')[2].get('table').get('tableRows'):
            term = row.get('tableCells')[0].get('content')[0].get('paragraph').get('elements')[0].get('textRun').get('content')
            term = term.strip()
            if lowercase:
                term = term.lower()
            terms.append(term)

        return terms

    def get_definitions(self):
        '''
        This function returns the terms in the right hand column of a table.
        '''

        definitions = []
        document = self.service.documents().get(documentId=self.DOCUMENT_ID).execute()

        for row in document.get("body").get('content')[2].get('table').get('tableRows'):
            definition = row.get('tableCells')[1].get('content')[0].get('paragraph').get('elements')[0].get('textRun').get('content')
            definition = definition.strip()
            definitions.append(definition)

        return definitions            

    def alphabetize(self):
        '''
        This function alphabetizes the first table in the document.
        '''

        unsorted_terms = self.get_terms(lowercase=False)
        unsorted_definitions = self.get_definitions()

        sorted_values = sort(unsorted_terms.copy(), unsorted_definitions.copy())
        sorted_terms = sorted_values[0]
        sorted_definitions = sorted_values[1]

        for i in range(len(unsorted_definitions)):
            self.replace_text(unsorted_definitions[i], '^' + str(i))

        self.update_file()

        for i in range(len(unsorted_terms)):
            self.replace_text(unsorted_terms[i], '*' + str(i))

        self.update_file()

        for i in range(len(sorted_terms) - 1, -1, -1):
            self.replace_text('*' + str(i), sorted_terms[i])

        self.update_file()

        for i in range(len(sorted_definitions) - 1, -1, -1):
            self.replace_text('^' + str(i), sorted_definitions[i])

        self.update_file()

def sort(terms, definitions):
    moved = True

    while moved:
        moved = False

        for i in range(len(terms) - 1):
            if terms[i] > terms[i+1]:
                terms[i], terms[i+1] = terms[i+1], terms[i]
                definitions[i], definitions[i+1] = definitions[i+1], definitions[i]
                moved = True

    return[terms, definitions]
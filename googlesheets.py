

from __future__ import print_function
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class GoogleSheets:
    # The ID and range of your spreadsheet.
    spreadsheet_id = 'YOUR_SPREADSHEET_ID'
    range_ = 'YOUR_RANGE'

    request = None

    def get_words(self):
        if not self.request:
            print('Instantiate class')
        else:
            result = self.request.get(spreadsheetId=self.spreadsheet_id, range=self.range_).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')
                return

            return values

    def write_to_sheet(self, definitions):
        if not self.request or not definitions:
            print('Instantiate class and make sure term and definition exist')
        else:
            value_range_body = {
                "range": self.range_,
                "majorDimension": "ROWS",
                "values": definitions
            }

            # How the input data should be interpreted.
            value_input_option = 'USER_ENTERED'

            insert_data_option = 'INSERT_ROWS'

            request = self.request.append(spreadsheetId=self.spreadsheet_id, range=self.range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
            response = request.execute()

            print('{0} rows appended.'.format(response.get('updates').get('updatedRows')))
    
    def update_sheet(self, data):
        if not self.request or not data:
            print('Instantiate class and make sure term and definition exist')
        else:
            value_range_body = {
                "value_input_option": 'USER_ENTERED',
                "data": data
            }

            request = self.request.batchUpdate(spreadsheetId=self.spreadsheet_id, body=value_range_body)
            response = request.execute()

            print('{0} rows updated.'.format(len(response.get('responses'))))

    def __init__(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('sheets', 'v4', credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()

            self.request = service.spreadsheets().values()
            
        except HttpError as err:
            print(err)


def __int__(self):
    self.data = []
from email import message
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.timer import make_readable_date, make_readable_time

# If modifying these scopes, delete the file utils/sheets/token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1UpkoZjFpj5pOdtBEtslKq0eAqmGjZQ7grYaEmiaPVNU"

def getService():
    creds = None
    if os.path.exists('utils/sheets/token.json'):
        creds = Credentials.from_authorized_user_file('utils/sheets/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'utils/sheets/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('utils/sheets/token.json', 'w') as token:
            token.write(creds.to_json())

    return build('sheets', 'v4', credentials=creds)

service = getService()

frequency_answers = [
    '• Реже, чем раз в неделю',
    '• Один или несколько раз в неделю',
    '• Один раз в день ',
    '• Несколько раз на дню ',
]

def save_user_data(user_data):
    user_data_type = user_data['servey_type']
    
    match user_data_type:
        case 'entry':
            save_entry_servey(user_data)
        case 'daily':
            save_daily_servey(user_data)
        case 'weekly':
            save_weekly_servey(user_data)
    
def save_entry_servey(user_data):
    user_id = user_data['user_id']
    date = make_readable_date(user_data['date'])

    frequency = user_data['frequency']
    severity = user_data['severity']

    answers = [
        str(frequency) + frequency_answers[int(frequency) - 1],
        str(severity)
               ]

    answers.append(date)
    
    body = {
        'values': [answers]
    }
    print(body)
    service.spreadsheets().values().append(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f'Респ {user_id}!A8',
        valueInputOption="RAW", body=body, insertDataOption='INSERT_ROWS').execute()

def save_daily_servey(user_data):
    user_id = user_data['user_id']
    date = make_readable_date(user_data['date'])

    att = 'answer_time'
    at = 'answer'

    answers: list = [
        f'({make_readable_time(user_data[i][att])})  {user_data[i][at]}'
        for i in ['a1', 'a2', 'a3', 'a4', 'a5', 'a6'] if i in user_data
        ]

    answers.insert(0, date)
    answers.insert(0, '')
    answers.insert(0, '')

    body = {
        'values': [answers]
    }
    print(body)
    service.spreadsheets().values().append(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f'Респ {user_id}!A8',
        valueInputOption="RAW", body=body, insertDataOption='INSERT_ROWS').execute()

def save_weekly_servey(user_data):
    user_id = user_data['user_id']
    date = make_readable_date(user_data['date'])

    att = 'answer_time'
    at = 'answer'

    answers: list = [
        f'({make_readable_time(user_data[i][att])})  {user_data[i][at]}'
        for i in ['a1', 'a2', 'a3', 'a4', 'a5', 'a6'] if i in user_data
        ]
    
    answers.insert(0, '')
    answers.insert(0, '')
    answers.insert(0, '')
    answers.insert(0, '')
    answers.insert(0, '')
    answers.insert(0, date)
    answers.insert(0, '')
    answers.insert(0, '')

    body = {
        'values': [answers]
    }
    print(body)
    service.spreadsheets().values().append(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f'Респ {user_id}!A8',
        valueInputOption="RAW", body=body, insertDataOption='INSERT_ROWS').execute()

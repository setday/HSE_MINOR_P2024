from email import message
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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

frequency_answers = [
    '• Реже, чем раз в неделю',
    '• Один или несколько раз в неделю',
    '• Один раз в день ',
    '• Несколько раз на дню ',
]

def add_start_message(service, user_id, message):
    answers: list = message.split('\n\n')

    for i in range(1, len(answers)):
        answers[i] = answers[i].split('\nA ')[1]
    print(answers)

    answers.append(answers.pop(0))

    answers[0] += frequency_answers[int(answers[0][-1]) - 1]

    body = {
        'values': [answers]
    }
    service.spreadsheets().values().append(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f'Респ {user_id}!A8',
        valueInputOption="RAW", body=body, insertDataOption='INSERT_ROWS').execute()

def add_daily_servey_message(service, user_id, message):
    answers: list = message.split('\n\n')

    for i in range(1, len(answers)):
        answers[i] = answers[i].split('\nA ')[1]
    print(answers)

    answers.insert(0, '')
    answers.insert(0, '')

    body = {
        'values': [answers]
    }
    service.spreadsheets().values().append(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f'Респ {user_id}!A8',
        valueInputOption="RAW", body=body, insertDataOption='INSERT_ROWS').execute()
    
def add_weekly_servey_message(service, user_id, message):
    answers: list = message.split('\n\n')

    for i in range(1, len(answers)):
        answers[i] = answers[i].split('\nA ')[1]
    print(answers)

    answers.insert(1, '')
    answers.insert(1, '')
    answers.insert(1, '')
    answers.insert(1, '')
    answers.insert(1, '')

    answers.insert(0, '')
    answers.insert(0, '')

    body = {
        'values': [answers]
    }
    service.spreadsheets().values().append(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f'Респ {user_id}!A8',
        valueInputOption="RAW", body=body, insertDataOption='INSERT_ROWS').execute()
    
def add_message(service, message):
    parts = message.split('\n\n', 1)
    message = parts[1]
    service_info = parts[0]
    service_info = service_info.split(' ')
    user_id = service_info[5]

    if service_info[2] == '(входная)':
        add_start_message(service, user_id, message)
    elif service_info[2] == '(дневная)':
        add_daily_servey_message(service, user_id, message)
    elif service_info[2] == '(недельная)':
        add_weekly_servey_message(service, user_id, message)
    else:
        print('Unknown type')


if __name__ == "__main__":
    service = getService()
    
    messages = [
    ]

    for message in messages:
        try:
            add_message(service, message)
        except Exception as e:
            print(e)
            print('Error with message:', message)
            continue
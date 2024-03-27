from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

import base64
from googleapiclient import errors

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
attachments_dir = './attachments/taco/'


def delete_existing_pdfs(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory, filename)
            try:
                os.remove(file_path)
                print(f'Deleted {file_path}')
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

# Usage
delete_existing_pdfs(attachments_dir)

def get_gmail_service():
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=51421)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

service = get_gmail_service()
# Replace 'your specific address' with the actual content you're searching for
after_date = "2024/01/01"  # Start of the date range
before_date = "2024/01/31"  # End of the date range
# query = f'after:{after_date} before:{before_date}'

query = f'from:noreply@swiggy.in subject:Swiggy "560034" after:{after_date}'
results = service.users().messages().list(userId='me', q=query).execute()
messages = results.get('messages', [])

print(messages)

os.makedirs(attachments_dir, exist_ok=True)


# Further code to process each message, extract and download attachments


def download_attachments(service, user_id, message_id, store_dir):
    """
    Download all attachments from a given email.
    """
    try:
        message = service.users().messages().get(userId=user_id, id=message_id).execute()

        for part in message['payload']['parts']:
            if part['filename']:
                if 'data' in part['body']:
                    data = part['body']['data']
                else:
                    att_id = part['body']['attachmentId']
                    att = service.users().messages().attachments().get(userId=user_id, messageId=message_id, id=att_id).execute()
                    data = att['data']
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                path = os.path.join(store_dir, part['filename'])

                with open(path, 'wb') as f:
                    f.write(file_data)

    except errors.HttpError as error:
        print(f'An error occurred: {error}')

# Assuming `service` is the Gmail API service instance from Step 1
user_id = 'me'
store_dir = './attachments'
if not os.path.exists(store_dir):
    os.makedirs(store_dir)

for message in messages:
    message_id = message['id']
    download_attachments(service, user_id, message_id, store_dir)
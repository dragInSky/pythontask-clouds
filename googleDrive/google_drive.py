from __future__ import print_function

import mimetypes
import os.path
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive']


def get_credentials():
    creds = None
    if os.path.exists('googleDrive/token.json'):
        creds = Credentials.from_authorized_user_file('googleDrive/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('googleDrive/token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def upload_file(filename):
    creds = get_credentials()

    try:
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {'name': filename}
        media = MediaFileUpload(filename,
                                mimetype=mimetypes.MimeTypes().guess_type(filename)[0])
        service.files().create(body=file_metadata, media_body=media,
                               fields='id').execute()
    except HttpError as e:
        print(f'Exception: {e}')

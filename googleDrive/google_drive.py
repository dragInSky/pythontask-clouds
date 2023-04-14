from __future__ import print_function

import mimetypes
import os.path

from typing import Any
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive']


def get_credentials() -> Credentials:
    creds = None
    if os.path.exists('googleDrive/token.json'):
        creds = Credentials.from_authorized_user_file('googleDrive/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('googleDrive/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('googleDrive/token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def upload_file(file_fullpath: str, folder_id: str):
    name = file_fullpath.split('/')[-1]
    file_path = file_fullpath.removesuffix(name)
    _upload_file(file_path, name, folder_id)


def _upload_file(file_path: str, name: str, folder_id: str):
    creds = get_credentials()

    try:
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': name,
            'parents': [folder_id]
        }

        file_fullpath = os.path.join(file_path, name)
        media = MediaFileUpload(file_fullpath, mimetype=mimetypes.MimeTypes().guess_type(file_fullpath)[0])
        service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    except HttpError as e:
        print(f'Exception: {e}')


def upload_folder(folder_path: str) -> dict[str, Any]:
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    parents_id = {}

    for root, _, files in os.walk(folder_path, topdown=True):
        last_dir = root.split('/')[-1]
        pre_last_dir = root.split('/')[-2]
        if pre_last_dir not in parents_id.keys():
            pre_last_dir = []
        else:
            pre_last_dir = parents_id[pre_last_dir]

        folder_metadata = {
            'name': last_dir,
            'parents': [pre_last_dir],
            'mimeType': 'application/vnd.google-apps.folder'
        }

        create_folder = service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = create_folder.get('id', [])

        for name in files:
            _upload_file(root, name, folder_id)

        parents_id[last_dir] = folder_id

    return parents_id

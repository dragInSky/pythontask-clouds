from __future__ import print_function

import mimetypes
import os.path
import io

from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tabulate import tabulate


class GoogleDrive:
    _SCOPES = ['https://www.googleapis.com/auth/drive']
    _TOKEN_PATH = 'googleDrive/token.json'
    _CREDS_PATH = 'googleDrive/credentials.json'

    _creds = None
    _service = None

    def __init__(self):
        if os.path.exists(self._TOKEN_PATH):
            self._creds = Credentials.from_authorized_user_file(self._TOKEN_PATH, self._SCOPES)
        if not self._creds or not self._creds.valid:
            if self._creds and self._creds.expired and self._creds.refresh_token:
                self._creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self._CREDS_PATH, self._SCOPES)
                self._creds = flow.run_local_server(port=0)
            with open(self._TOKEN_PATH, 'w') as token:
                token.write(self._creds.to_json())

        self._service = build('drive', 'v3', credentials=self._creds)

    def _upload_file(self, file_fullpath: str, folder_id: str):
        try:
            name = file_fullpath.split('/')[-1]

            file_metadata = {
                'name': name,
                'parents': [folder_id]
            }

            media = MediaFileUpload(file_fullpath, mimetype=mimetypes.MimeTypes().guess_type(file_fullpath)[0])
            self._service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        except HttpError as e:
            print(f'Exception: {e}')

    def _upload_folder(self, folder_path: str):
        try:
            parents_id = {}

            for dir_path, _, filenames in os.walk(folder_path, topdown=True):
                last_dir = dir_path.split('/')[-1]
                pre_last_dir = dir_path.split('/')[-2]

                # Если родительская папка еще не создана на диске
                if pre_last_dir not in parents_id.keys():
                    pre_last_dir = []
                else:
                    # Если у папки last_dir есть родительская папка,
                    # то сохраняем id родительской папки для метаданных
                    pre_last_dir = parents_id[pre_last_dir]

                folder_metadata = {
                    'name': last_dir,
                    'parents': [pre_last_dir],
                    'mimeType': 'application/vnd.google-apps.folder'
                }

                create_folder = self._service.files().create(body=folder_metadata, fields='id').execute()
                folder_id = create_folder.get('id', [])
                parents_id[last_dir] = folder_id

                for name in filenames:
                    file_fullpath = os.path.join(dir_path, name)
                    self._upload_file(file_fullpath=file_fullpath, folder_id=folder_id)

        except HttpError as e:
            print(f'Exception: {e}')

    def upload(self, path: str, folder_id: str):
        if '.' in path:
            self._upload_file(path, folder_id)
        else:
            self._upload_folder(path)

    def file_listing(self):
        try:
            results = self._service.files().list(
                fields="nextPageToken, files(id, name, size, modifiedTime)"
            ).execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
            else:
                output = list(list())
                for item in items:
                    size = 'folder' if 'size' not in item else item['size']
                    modified_time = item['modifiedTime'].replace('T', ' ')
                    modified_time = modified_time[:modified_time.index('.')]
                    row = [
                        '{0}'.format(item['name']),
                        '{0}'.format(item['id']),
                        '{0}'.format(size),
                        '{0}'.format(modified_time)
                    ]
                    output.append(row)
                print(tabulate(output, headers=['name', 'id', 'size', 'last modify time']))

        except HttpError as e:
            print(f'Exception: {e}')

    def download_file(self, filename: str, file_id: str, download_dir: str):
        try:
            request = self._service.files().get_media(fileId=file_id)
            file = io.FileIO(os.path.join(download_dir, filename), 'wb')
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(F'Download {int(status.progress() * 100)}.')

        except HttpError as e:
            print(f'Exception: {e}')

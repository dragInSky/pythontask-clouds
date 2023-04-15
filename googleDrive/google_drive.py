from __future__ import print_function

import mimetypes
import os.path

from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


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

    def upload_file(self, file_fullpath: str, folder_id: str = 'root'):
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

    def upload_folder(self, folder_path: str):
        try:
            parents_id = {}

            for dir_path, _, filenames in os.walk(folder_path, topdown=True):
                last_dir = dir_path.split('/')[-1]
                pre_last_dir = dir_path.split('/')[-2]
                print(last_dir, pre_last_dir)
                if pre_last_dir not in parents_id.keys():
                    pre_last_dir = []
                else:
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
                    self.upload_file(file_fullpath, folder_id)
        except HttpError as e:
            print(f'Exception: {e}')


# SCOPES = ['https://www.googleapis.com/auth/drive']
#
#
# def get_credentials() -> Credentials:
#     creds = None
#     if os.path.exists('googleDrive/token.json'):
#         creds = Credentials.from_authorized_user_file('googleDrive/token.json', SCOPES)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file('googleDrive/credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open('googleDrive/token.json', 'w') as token:
#             token.write(creds.to_json())
#     return creds
#
#
# def upload_file(file_fullpath: str, folder_id: str = 'root'):
#     name = file_fullpath.split('/')[-1]
#     file_path = file_fullpath.removesuffix(name)
#     _upload_file(file_path, name, folder_id)
#
#
# def _upload_file(file_path: str, name: str, folder_id: str):
#     try:
#         creds = get_credentials()
#         service = build('drive', 'v3', credentials=creds)
#
#         file_metadata = {
#             'name': name,
#             'parents': [folder_id]
#         }
#
#         file_fullpath = os.path.join(file_path, name)
#         media = MediaFileUpload(file_fullpath, mimetype=mimetypes.MimeTypes().guess_type(file_fullpath)[0])
#         service.files().create(body=file_metadata, media_body=media, fields='id').execute()
#     except HttpError as e:
#         print(f'Exception: {e}')
#
#
# def _inner_upload_folder(last_dir: str, pre_last_dir: str, parents_id: dict[str, Any], root: str, files: list):
#     creds = get_credentials()
#     service = build('drive', 'v3', credentials=creds)
#
#     folder_metadata = {
#         'name': last_dir,
#         'parents': [pre_last_dir],
#         'mimeType': 'application/vnd.google-apps.folder'
#     }
#
#     create_folder = service.files().create(body=folder_metadata, fields='id').execute()
#     folder_id = create_folder.get('id', [])
#     parents_id[last_dir] = folder_id
#
#     for name in files:
#         _upload_file(root, name, folder_id)
#
#
# def upload_folder(folder_path: str):
#     try:
#         parents_id = {}
#
#         for root, _, files in os.walk(folder_path, topdown=True):
#             print(root, _, files)
#             last_dir = root.split('/')[-1]
#             pre_last_dir = root.split('/')[-2]
#             if pre_last_dir not in parents_id.keys():
#                 pre_last_dir = []
#             else:
#                 pre_last_dir = parents_id[pre_last_dir]
#
#             _inner_upload_folder(last_dir, pre_last_dir, parents_id, root, files)
#     except HttpError as e:
#         print(f'Exception: {e}')
#
# # def get_os_tree(folder_path: str, os_tree: list):
# #     root_len = len(folder_path.split(os.path.sep)[0:-2])
# #     for root, dirs, files in os.walk(folder_path, topdown=True):
# #         for name in dirs:
# #             var_path = '/'.join(root.split('/')[root_len + 1:])
# #             os_tree.append(os.path.join(var_path, name))
# #
# #
# # def get_cloud_tree(folder_name: str, root: str, parents_id: dict[str, Any], cloud_tree: list):
# #     try:
# #         creds = get_credentials()
# #         service = build('drive', 'v3', credentials=creds)
# #
# #         folder_id = parents_id[folder_name]
# #
# #         results = service.files().list(
# #             pageSize=100,
# #             q=("%r in parents and mimeType = \
# #             'application/vnd.google-apps.folder'and trashed != True" % folder_id)
# #         ).execute()
# #
# #         items = results.get('files', [])
# #         root += folder_name + os.path.sep
# #
# #         for item in items:
# #             parents_id[item['name']] = item['id']
# #             cloud_tree.append(root + item['name'])
# #             folder_name = item['name']
# #             get_cloud_tree(folder_name, root, parents_id, cloud_tree)
# #     except HttpError as e:
# #         print(f'Exception: {e}')
# #
# #
# # def folders_sync(folder_path: str, upload_folders: list, parents_id: dict[str, Any]):
# #     for folder_dir in upload_folders:
# #         var = os.path.join(folder_path.split(os.path.sep)[-1]) + os.path.sep
# #         root = var + folder_dir
# #         last_dir = folder_dir.split(os.path.sep)[-1]
# #         pre_last_dir = folder_dir.split(os.path.sep)[-2]
# #
# #         files = [f for f in os.listdir(root) if os.path.isfile(os.path.join(root, f))]
# #
# #         _inner_upload_folder(last_dir, pre_last_dir, parents_id, root, files)
# #
# #
# # def pc_cloud_sync(folder_path: str, folder_name: str, root: str, parents_id):
# #     os_tree, cloud_tree = [], []
# #     get_os_tree(folder_name, os_tree)
# #     get_cloud_tree(folder_name, root, parents_id, cloud_tree)
# #     remove_folders = list(set(cloud_tree).difference(set(os_tree)))
# #     upload_folders = list(set(os_tree).difference(set(cloud_tree)))
# #     exact_folders = list(set(os_tree).intersection(set(cloud_tree)))
# #
# #     upload_folders = sorted(upload_folders)
# #     folders_sync(folder_path, upload_folders, parents_id)

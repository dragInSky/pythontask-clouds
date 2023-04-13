import os
from datetime import datetime
from requests_oauthlib import OAuth2Session
from requests import get, post, put, delete
import config

auth_url = "https://oauth.yandex.ru/authorize"
token_url = "https://oauth.yandex.ru/token"


def get_user_token():
    access_token = ""
    oauth = OAuth2Session(client_id=config.client_id)
    authorization_url, state = oauth.authorization_url(auth_url, force_confirm="true")
    print("Перейдите по ссылке, авторизуйтесь и скопируйте код:", authorization_url)
    code = input("Вставьте одноразовый код: ")
    try:
        token = oauth.fetch_token(token_url=token_url,
                                  code=code,
                                  client_secret=config.client_secret)
        access_token = token["access_token"]
    except:
        print("Ошибка! Попробуйте ещё раз")
    return access_token


def info_disk(token):
    """
        Инфа о диске
    """
    headers = {"Authorization": f"OAuth {token}"}
    r = get("https://cloud-api.yandex.net/v1/disk", headers=headers)
    print(r.json())


def create_folder(token, name_folder):
    """
    :param token: токен пользователя, который был получен при авторизации
    :param name_folder: имя папки
    """
    headers = {"Authorization": f"OAuth {token}"}
    params = {"path": f"{name_folder}"}
    r = put("https://cloud-api.yandex.net/v1/disk/resources", headers=headers, params=params)
    print(r)


def upload_file(token, name_folder, name_file):
    """
    :param token: токен пользователя, который был получен при авторизации
    :param name_folder: имя папки на диске
    :param name_file: имя загружаемого файла
    """
    headers = {"Authorization": f"OAuth {token}"}
    params = {"path": f"{name_folder}/{name_file}"}
    r = get("https://cloud-api.yandex.net/v1/disk/resources/upload",
            headers=headers, params=params)
    print(r)
    href = r.json()["href"]
    files = {"file": open(f"{name_file}", "rb")}
    r = put(href, files=files)
    print(r)


# backup создает папки, но не загружает в них файлы
def backup(token, path_disk, path_load):
    date_folder = '{0}_{1}'.format(path_load.split('\\')[-1], datetime.now().strftime("%Y.%m.%d-%H.%M.%S"))
    create_folder(token, path_disk)
    for address, _, files in os.walk(path_load):
        create_folder(token,
                      '{0}/{1}/{2}'.format(path_disk, date_folder,
                                           address.replace(path_load, "")[1:].replace("\\", "/")))
        for file in files:
            upload_file(token, '{0}/{1}'.format(address, file),
                        '{0}/{1}{2}/{3}'.format(path_disk, date_folder,
                                                address.replace(path_load, "").replace("\\", "/"),
                                                file))


user_code = get_user_token()
create_folder(user_code, 'test_cloud_path_for_disk')
upload_file(user_code, 'test_cloud_path_for_disk', 'test.txt')
# info_disk(user_code)
# backup(user_code, "Тестовая папка для тестового бэкапа", "C:\\pythontask-clouds")
# create_folder(user_code, "Тестовая папка для тестового файла")

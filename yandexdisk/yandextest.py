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
    r = get(f"{config.YANDEX_URL}", headers=headers)
    print(r.json())


def create_folder(token, name_folder):
    """
    :param token: токен пользователя, который был получен при авторизации
    :param name_folder: имя папки
    """
    headers = {"Authorization": f"OAuth {token}"}
    params = {"path": f"{name_folder}"}
    r = put(f"{config.YANDEX_URL}/resources", headers=headers, params=params)
    print(r)


def upload_file(token, local_path, cloud_path):
    """
    :param token: токен пользователя, который был получен при авторизации
    :param local_path: локальный путь к файлу
    :param cloud_path: путь в облаке
    """
    headers = {"Authorization": f"OAuth {token}"}
    params = {"path": cloud_path}
    r = get(f"{config.YANDEX_URL}/resources/upload",
            headers=headers, params=params)
    href = r.json()["href"]
    with open(local_path, 'rb') as f:
        r = put(href, data=f)
    print(r)


def backup(token, path_disk, path_load):
    date_folder = '{0}_{1}'.format(path_load.split('\\')[-1], datetime.now().strftime("%Y.%m.%d-%H.%M.%S"))
    create_folder(token, path_disk)
    for address, _, files in os.walk(path_load):
        create_folder(token,
                      '{0}/{1}/{2}'.format(path_disk, date_folder,
                                           address.replace(path_load, "")[1:].replace("\\", "/")))
        for file in files:
            upload_file(token, '{0}/{1}'.format(address, file), '{0}/{1}{2}/{3}'.format(path_disk, date_folder,
                                                                                        address.replace(path_load,
                                                                                                        "").replace(
                                                                                            "\\", "/"),
                                                                                        file))



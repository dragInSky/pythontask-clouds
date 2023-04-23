import os
from datetime import datetime
from requests_oauthlib import OAuth2Session
from requests import get, put


class YandexDisk:
    _AUTH_URL = "https://oauth.yandex.ru/authorize"
    _TOKEN_URL = "https://oauth.yandex.ru/token"
    _YANDEX_URL = "https://cloud-api.yandex.net/v1/disk"
    client_id = "0920941bb5d742a99a1aff5aaddeb730"
    client_secret = "48ede7d38db949929c0271c1af9c2ac1"
    token_user = None

    def user_token(self):
        oauth = OAuth2Session(client_id=self.client_id)
        authorization_url, state = oauth.authorization_url(self._AUTH_URL, force_confirm="true")
        print("Перейдите по ссылке, авторизуйтесь и скопируйте код:", authorization_url)
        code = input("Вставьте одноразовый код: ")
        try:
            token = oauth.fetch_token(token_url=self._TOKEN_URL,
                                      code=code,
                                      client_secret=self.client_secret)
            self.token_user = token["access_token"]
        except Exception as ex:
            print(ex)

    def info_disk(self):
        headers = {"Authorization": f"OAuth {self.token_user}"}
        r = get(self._YANDEX_URL, headers=headers)
        print(r)

    def create_folder(self, folder_name):
        """
        :param folder_name: имя будущей папки на облаке
        """
        headers = {"Authorization": f"OAuth {self.token_user}"}
        params = {"path": f"{folder_name}"}
        r = put(f"{self._YANDEX_URL}/resources", headers=headers, params=params)
        print(r)

    def upload_file(self, local_path, in_cloud_name):
        """
        :param local_path: локальный путь до файла
        :param in_cloud_name: имя файла на облаке, если поле будет пусто, то имя
                                файла будет взято с локального пути
        """
        if in_cloud_name == '':
            in_cloud_name = local_path.split('/')[-1]
        headers = {"Authorization": f"OAuth {self.token_user}"}
        params = {"path": in_cloud_name}
        r = get(f"{self._YANDEX_URL}/resources/upload",
                headers=headers, params=params)
        print(r)
        href = r.json()["href"]
        with open(local_path, 'rb') as f:
            r = put(href, data=f)

    def upload_folder(self, local_path):
        """
        :param local_path: путь до папки
        """
        try:
            date_folder = '{0}_{1}'.format(local_path.split('/')[-1], datetime.now().strftime("%Y.%m.%d-%H.%M.%S"))
            for address, _, files in os.walk(local_path):
                self.create_folder(
                    '{0}/{1}'.format(date_folder,
                                     address.replace(local_path, "")[1:].replace("\\", "/")))
                for file in files:
                    self.upload_file(
                        '{0}/{1}'.format(address, file),
                        '{0}/{1}{2}/{3}'.format("", date_folder, address.replace(local_path, "").replace("\\", "/"),
                                                file))
        except Exception as ex:
            print(ex)

    def download_file(self, local_path, cloud_path):
        """
        :param local_path: путь до файла
        :param cloud_path: имя файла на облаке
        """
        try:
            headers = {"Authorization": f"OAuth {self.token_user}"}
            params = {'path': cloud_path}
            r1 = get(f'{self._YANDEX_URL}/resources/download', params=params, headers=headers)
            link = r1.json()['href']
            r2 = get(link, headers=headers)
            file_name = cloud_path.split('/')[-1]
            with open(f'{local_path}/{file_name}', 'wb') as f:
                f.write(r2.content)
        except Exception as ex:
            print(ex)


# YD.download_file("C:\\Users\\Sergey\\Desktop", "test.txt")

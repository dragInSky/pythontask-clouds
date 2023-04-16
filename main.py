import config
import yandexdisk.yandextest
import argparse

from googleDrive.google_drive import GoogleDrive
from yandexdisk.yandextest import upload_file, get_user_token, backup


def main():
    parser = argparse.ArgumentParser(description='google and yandex clouds')
    parser.add_argument(
        '-g',
        '--googleDrive',
        action="store_true",
        help='choosing a google drive cloud'
    )
    parser.add_argument(
        '-y',
        '--yandexDisk',
        action="store_true",
        help='choosing a yandex disk cloud'
    )
    args = parser.parse_args()

    if args.googleDrive:
        print('google')

        # file_path = '\\Users\\draginsky\\PycharmProjects\\pythontask-clouds\\googleDrive\\Hello.txt'
        folder_path = '/Users/draginsky/PycharmProjects/pythontask-clouds/download'

        # file_path = file_path.replace('\\', '/')
        folder_path = folder_path.replace('\\', '/')

        GD = GoogleDrive()
        GD.file_listing()

        GD.download_file(
            '/Users/draginsky/PycharmProjects/pythontask-clouds/download',
            'SCR-20230320-qiji.png',
            '1VGUohkQ951DLIeD2yJQJVgWsBtdV8idg'
        )
        # GD.upload_file(file_path)
        # GD.upload_folder(folder_path)
    elif args.yandexDisk:
        print('yandex')
        user_code = get_user_token()
        backup(user_code, "Тестовая папка для тестового бэкапа", "C:\\pythontask-clouds")


if __name__ == '__main__':
    main()

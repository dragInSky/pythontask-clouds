import config
import yandexdisk.yandextest
import argparse

from googleDrive.google_drive import upload_file
from yandexdisk.yandextest import upload_file, get_user_token, backup
from googleDrive.google_drive import upload_folder


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
        upload_file('/Users/draginsky/PycharmProjects/pythontask-clouds/googleDrive/Hello.txt', 'root')
        upload_file('/Users/draginsky/PycharmProjects/pythontask-clouds/googleDrive/SCR-20230320-qiji.png', 'root')

        upload_folder('/Users/draginsky/PycharmProjects/pythontask-clouds/yandexdisk')
    elif args.yandexDisk:
        print('yandex')
        user_code = get_user_token()
        backup(user_code, "Тестовая папка для тестового бэкапа", "C:\\pythontask-clouds")


if __name__ == '__main__':
    main()

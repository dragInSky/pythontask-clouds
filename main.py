from googleDrive.google_drive import upload_file
from yandexdisk.yandextest import upload_file, get_user_token, backup
import config
from googleDrive.google_drive import upload_folder
import yandexdisk.yandextest
import argparse


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
        upload_file('/Users/draginsky/PycharmProjects/pythontask-clouds/googleDrive/Hello.txt', 'root')
        upload_file('/Users/draginsky/PycharmProjects/pythontask-clouds/googleDrive/SCR-20230320-qiji.png', 'root')

        # upload_folder('/Users/draginsky/PycharmProjects/pythontask-clouds/yandexdisk')
    elif args.yandexDisk:
        pass


if __name__ == '__main__':
    main()

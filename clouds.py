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
    parser.add_argument(
        '-l',
        '--listing',
        action="store_true",
        help='display list of cloud files'
    )
    parser.add_argument(
        '-u',
        '--upload',
        nargs='+',
        action='store',
        type=str,
        help='upload a file or folder to the cloud'
    )
    parser.add_argument(
        '-d',
        '--download',
        nargs='+',
        action='store',
        type=str,
        help='upload a file from the cloud'
    )
    args = parser.parse_args()

    if args.googleDrive:
        print('google\n')

        GD = GoogleDrive()

        if args.listing:
            GD.file_listing()

# -u /Users/draginsky/PycharmProjects/pythontask-clouds/download/testFolder/Hello.txt 1SOFcPWd_Mgc44ywCFtmK41CuT3fDgDm-
        if args.upload:
            path = args.upload[0].replace('\\', '/')
            folder_id = 'root' if len(args.upload) < 2 else args.upload[1]
            GD.upload(path=path, folder_id=folder_id)

# -d SCR-20230320-qiji.png 1VGUohkQ951DLIeD2yJQJVgWsBtdV8idg /Users/draginsky/PycharmProjects/pythontask-clouds/download
        if len(args.download) >= 2:
            filename = args.download[0]
            file_id = args.download[1]
            download_dir = '' if len(args.download) < 3 else args.download[2]
            GD.download_file(filename=filename, file_id=file_id, download_dir=download_dir)
    elif args.yandexDisk:
        print('yandex')
        user_code = get_user_token()
        backup(user_code, "Тестовая папка для тестового бэкапа", "C:\\pythontask-clouds")


if __name__ == '__main__':
    main()

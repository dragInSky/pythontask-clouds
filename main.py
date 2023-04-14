from googleDrive.google_drive import upload_file
from yandexdisk.yandextest import upload_file, get_user_token, backup
import config


def main():
    drive_choice = input()
    if drive_choice == 'google':
        upload_file('googleDrive/Hello.txt')
        upload_file('googleDrive/SCR-20230320-qiji.png')
    elif drive_choice == 'yandex':
        user_code = get_user_token()
        backup(user_code, "Тестовая папка для тестового бэкапа", "C:\\pythontask-clouds")


if __name__ == '__main__':
    main()

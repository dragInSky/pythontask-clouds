from googleDrive.google_drive import upload_file
import yandexdisk.yandextest


def main():
    drive_choice = input()
    if drive_choice == 'google':
        upload_file('googleDrive/Hello.txt')
        upload_file('googleDrive/SCR-20230320-qiji.png')
    elif drive_choice == 'yandex':
        pass


if __name__ == '__main__':
    main()

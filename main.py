from googleDrive.google_drive import upload_file
from googleDrive.google_drive import upload_folder
import yandexdisk.yandextest


def main():
    # drive_choice = input()
    # if drive_choice == 'google':


    # upload_file('/Users/draginsky/PycharmProjects/pythontask-clouds/googleDrive/Hello.txt', 'root')
    # upload_file('/Users/draginsky/PycharmProjects/pythontask-clouds/googleDrive/SCR-20230320-qiji.png', 'root')

    upload_folder('/Users/draginsky/PycharmProjects/pythontask-clouds/yandexdisk')


    # elif drive_choice == 'yandex':
    #     pass


if __name__ == '__main__':
    main()

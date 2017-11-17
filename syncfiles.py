import os

from dirsync import sync
from envparse import env
from pushover import Client
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

"""
    * Syncs with Google Drive
    * Syncs the SOURCE_DIR to the TARGET_DIR
    * Sends notifications as needed via Pushover
"""

env.read_envfile()

SOURCE_DIR = env('SOURCE_DIR')
TARGET_DIR = env('TARGET_DIR')
PUSHOVER_API_TOKEN = env('PUSHOVER_API_TOKEN')
PUSHOVER_USER_KEY = env('PUSHOVER_USER_KEY')
APP_NAME = env('APP_NAME')


def send_notification(title, msg):
    client = Client(PUSHOVER_USER_KEY, api_token=PUSHOVER_API_TOKEN)
    client.send_message(msg, title=title)


def run():
    # sync files from google drive
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    # make sure the source dir exists, exit if it doesn't
    if not os.path.exists(SOURCE_DIR):
        msg = "SOURCE_DIR {} doesn't exist!".format(SOURCE_DIR)
        print(msg)
        send_notification(
            '{} - ERROR'.format(APP_NAME),
            msg
        )
        exit(1)

    # make sure the target dir exists, create if it doesn't
    if not os.path.exists(TARGET_DIR):
        print("TARGET_DIR {} doesn't exist. Creating ...".format(TARGET_DIR))
        os.mkdir(TARGET_DIR)

    print('Syncing files ...')

    try:
        sync(SOURCE_DIR, TARGET_DIR, 'sync', purge=True)
        msg = 'Successful sync!'
        print(msg)
        send_notification(
            '{} - SYNC OK'.format(APP_NAME),
            msg
        )
    except Exception as e:
        msg = 'ERROR: {}'.format(str(e))
        print(msg)
        send_notification(
            '{} - SYNC FAILED'.format(APP_NAME),
            msg
        )


if __name__ == '__main__':
    run()

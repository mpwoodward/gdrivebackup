from datetime import datetime
import os
import tarfile
import time

from envparse import env
from pushover import Client

"""
    Archives TARGET_DIR and sends notifications via Pushover.
"""

env.read_envfile()

TARGET_DIR = env('TARGET_DIR')  # note that here TARGET_DIR is used as the SOURCE for the tarball
ARCHIVE_DIR = env('ARCHIVE_DIR')
DAYS_TO_RETAIN_ARCHIVES = env('DAYS_TO_RETAIN_ARCHIVES')
PUSHOVER_API_TOKEN = env('PUSHOVER_API_TOKEN')
PUSHOVER_USER_KEY = env('PUSHOVER_USER_KEY')
APP_NAME = env('APP_NAME')


def send_notification(title, msg):
    client = Client(PUSHOVER_USER_KEY, api_token=PUSHOVER_API_TOKEN)
    client.send_message(msg, title=title)


def run():
    # make sure the target dir exists, exit if it doesn't
    if not os.path.exists(TARGET_DIR):
        msg = "TARGET_DIR {} doesn't exist!".format(TARGET_DIR)
        print(msg)
        send_notification(
            '{} - ERROR'.format(APP_NAME),
            msg
        )
        exit(1)

    # make sure the archive dir exists, create if it doesn't
    if not os.path.exists(ARCHIVE_DIR):
        print("ARCHIVE_DIR {} doesn't exist. Creating ...")
        os.mkdir(ARCHIVE_DIR)

    print('Creating archive ...')

    try:
        archive_file_path = '{}/{}_archive.tgz'.format(
            ARCHIVE_DIR,
            datetime.now().strftime('%Y%m%d%H%M%S')
        )

        with tarfile.open(archive_file_path, 'w:gz') as tar:
            tar.add(TARGET_DIR, arcname=os.path.sep)

        msg = 'Successful archive!'
        print(msg)
        send_notification(
            '{} - ARCHIVE OK'.format(APP_NAME),
            msg
        )
    except Exception as e:
        msg = 'ERROR: {}'.format(str(e))
        print(msg)
        send_notification(
            '{} - ARCHIVE FAILED'.format(APP_NAME),
            msg
        )

    print('Removing old archives ...')

    try:
        n = time.time()
        d = int(DAYS_TO_RETAIN_ARCHIVES)

        for f in os.listdir(ARCHIVE_DIR):
            f = os.path.join(ARCHIVE_DIR, f)
            if os.stat(f).st_mtime < n - d * 86400:
                if os.path.isfile(f):
                    os.remove(f)

        print('Old archives removed.')
    except Exception as e:
        # only alert if the archives couldn't be removed so we don't run out of disk space
        msg = 'Removing old archives failed! {}'.format(str(e))
        print(msg)
        send_notification(
            '{} - REMOVING ARCHIVES FAILED'.format(APP_NAME),
            msg
        )


if __name__ == '__main__':
    run()

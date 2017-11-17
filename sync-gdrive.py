import argparse
import httplib2
import os

from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage


flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = 'JCD G-Drive Backup'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)

    return credentials


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)"
    ).execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{} ({})'.format(item['name'], item['id']))

    response = service.changes().getStartPageToken().execute()
    page_token = response.get('startPageToken')
    print('Start token: {}'.format(response.get('startPageToken')))

    while page_token:
        print('Getting changes ...')
        response = service.changes().list(pageToken=page_token, spaces='drive').execute()
        print(response.get('changes'))

        for change in response.get('changes'):
            print('Change found for file: {}'.format(change.get('fileId')))

        if 'newStartPageToken' in response:
            saved_start_page_token = response.get('newStartPageToken')

        page_token = response.get('nextPageToken')


if __name__ == '__main__':
    main()

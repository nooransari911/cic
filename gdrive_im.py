import os
import io
import json
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.cloud import secretmanager

ROOT="/opt/render/project/src/projects/compile image/"

# Configuration
SECRET_ID = 'projects/927511831564/secrets/wire_service_account_json/versions/latest'
FOLDER_ID = '1zSQOhdq3dv02PPyoqFapnZI0fx43jo_u'  # Update with your folder ID
DEST_DIR = f'{ROOT}static/image'  # Temp directory in Cloud Functions


def get_secret():
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=SECRET_ID)
    secret_payload = response.payload.data.decode('UTF-8')
    return secret_payload


def download_files():
    # Fetch and load credentials
    # secret_json = get_secret()
    secret_json = os.getenv ("GOOGLE_APPLICATION_CREDENTIALS")
    
    creds = service_account.Credentials.from_service_account_info(
        json.loads(secret_json), scopes=['https://www.googleapis.com/auth/drive.readonly'])
    service = build('drive', 'v3', credentials=creds)

    # List files in folder
    query = f"'{FOLDER_ID}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])

    if not files:
        return 'No files found.'

    # Download each file
    for file in files:
        request = service.files().get_media(fileId=file['id'])
        file_path = os.path.join(DEST_DIR, file['name'])
        with io.FileIO(file_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Downloading {file['name']} {int(status.progress() * 100)}%.")

    return 'All files downloaded successfully.'


if (__name__=="__main__"):
    download_files()

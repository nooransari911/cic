from flask import Flask, render_template, send_file, url_for
import io
import os
import json
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.cloud import secretmanager



# Example images stored in memory

images = {}
SECRET_ID = 'projects/927511831564/secrets/wire_service_account_json/versions/latest'


def get_secret():
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=SECRET_ID)
    secret_payload = response.payload.data.decode('UTF-8')
    return secret_payload



def get_images_from_drive(folder_id):
    #secret_json = get_secret()
    
    secret_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    creds = service_account.Credentials.from_service_account_info(
        json.loads(secret_json), scopes=['https://www.googleapis.com/auth/drive.readonly'])
    service = build('drive', 'v3', credentials=creds)
    
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])

    if not files:
        return 'No files found.'

    # Dictionary to store images in binary/raw form with unique IDs
    global images
    images = {}

    # Download each file into memory
    for file in files:
        request = service.files().get_media(fileId=file['id'])
        file_buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(file_buffer, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Downloading {file['name']} {int(status.progress() * 100)}%.")

        # Seek to the beginning of the BytesIO buffer
        file_buffer.seek(0)
        images[file['id']] = file_buffer.getvalue()

    return list(images.keys())






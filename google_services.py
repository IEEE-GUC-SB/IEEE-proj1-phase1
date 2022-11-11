import os
import pickle
from os import path

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


def create_service_with_api(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version

    SCOPES = [scope for scope in scopes[0]]

    cred = None

    pickle_file = f"token_{API_SERVICE_NAME}_{API_VERSION}.pickle"

    if os.path.exists(pickle_file):
        with open(pickle_file, "rb") as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, "wb") as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, "service created successfully")
        return service
    except Exception as e:
        print("Unable to connect.")
        print(e)
        return None


def create_service():
    CLIENT_SECRET_FILE = "credentials.json"
    API_Name = "drive"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    return create_service_with_api(CLIENT_SECRET_FILE, API_Name, API_VERSION, SCOPES)


SERVICE = create_service()


def upload_to_drive(file_name: str) -> str:
    """
    Upload file to drive, make its link shareable and then return it.
    """
    file_metadata = {"name": file_name}
    request_body = {"role": "reader", "type": "anyone"}
    IMAGES_PATH = "./qr_images"
    mime_type = "image/png"
    try:
        media = MediaFileUpload(
            path.join(IMAGES_PATH, "{0}").format(file_name), mimetype=mime_type
        )
        file = (
            SERVICE.files()
            .create(body=file_metadata, media_body=media, fields="webViewLink")
            .execute()
        )
        qr_code_link = file.get("webViewLink")
        qr_code_id = qr_code_link.split("/")[-2]

        response_permission = (
            SERVICE.permissions().create(fileId=qr_code_id, body=request_body).execute()
        )
    except HttpError as error:
        print(f"An error occurred: {error}")

    return qr_code_link

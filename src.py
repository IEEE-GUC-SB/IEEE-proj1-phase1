import os
import errno
from os import path

import pandas as pd
import qrcode
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer

from google_services import create_service
from data_generator import generate_dummy_data

IMAGES_PATH = "./qr_images"
ATTENDEES_CSV_PATH = "./attendees.csv"
ATTENDEES_XLSX_PATH = "./attendees.xlsx"
HEADERS = {
    "name": "Name",
    "email": "Email",
    "id": "ID",
    "phone": "Phone",
    "role": "Role",
}


def read_input_data():
    if path.exists(ATTENDEES_CSV_PATH):
        df = pd.read_csv(ATTENDEES_CSV_PATH)
    elif path.exists(ATTENDEES_XLSX_PATH):
        read_file = pd.read_excel(ATTENDEES_XLSX_PATH)
        read_file.to_csv(ATTENDEES_CSV_PATH, index=None, header=True)
        df = pd.DataFrame(pd.read_csv(ATTENDEES_CSV_PATH))
    else:
        if not path.exists(ATTENDEES_CSV_PATH):
           raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), ATTENDEES_CSV_PATH)
        elif not path.exists(ATTENDEES_XLSX_PATH):
           raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), ATTENDEES_XLSX_PATH) 

    return df

file_names = []

def qr_generating(data, idx):
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(
        image_factory=StyledPilImage,
        embeded_image_path="ieee_logo.png",
        module_drawer=RoundedModuleDrawer(),
        color_mask=RadialGradiantColorMask(),
    )
    img.save(path.join(IMAGES_PATH, "qr" + str(idx) + ".png"))
    file_names.append("qr" + str(idx) + ".png")


def retrieve_data():
    if not path.exists(IMAGES_PATH):
        os.mkdir(IMAGES_PATH)
    attributes = list(HEADERS.values())
    for row in range(0, len(df.index), 1):
        attendee_data = ""
        for attr in range(0, len(df.columns), 1):
            attendee_data += str(df.iloc[row, attr]) + "\n"
        qr_generating(attendee_data, row)


qr_codes_ids = []


def upload_to_drive(service):
    for file_name in file_names:
        mime_type = "image/png"
        file_metadata = {"name": file_name}
        try:
            media = MediaFileUpload(
                path.join(IMAGES_PATH, "{0}").format(file_name), mimetype=mime_type
            )
            file = (
                service.files()
                .create(body=file_metadata, media_body=media, fields="id")
                .execute()
            )
        except HttpError as error:
            print(f"An error occurred: {error}")

        qr_codes_ids.append(file.get("id"))


qr_codes_links = []


def get_qr_codes_urls(service):
    for qr_code_id in qr_codes_ids:
        request_body = {"role": "reader", "type": "anyone"}

        try:
            response_permission = (
                service.permissions()
                .create(fileId=qr_code_id, body=request_body)
                .execute()
            )
            response_shared_link = (
                service.files().get(fileId=qr_code_id, fields="webViewLink").execute()
            )
        except HttpError as error:
            print(f"An error occurred: {error}")

        qr_codes_links.append(response_shared_link.get("webViewLink"))


def insert_qr_codes():
    links = pd.Series(qr_codes_links)
    ids = pd.Series(qr_codes_ids)
    df["QR_code"] = links
    df["QR_code_id"] = ids
    df.to_excel("attendees_modified.xlsx")


def main():
    service = create_service()
    retrieve_data()
    upload_to_drive(service)
    get_qr_codes_urls(service)
    insert_qr_codes()


if __name__ == "__main__":
    main()

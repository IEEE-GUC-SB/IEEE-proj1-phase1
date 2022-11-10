import argparse
import errno
import os
from os import path

import pandas as pd
import qrcode
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer

from google_services import create_service

IMAGES_PATH = "./qr_images"
HEADERS = {
    "name": "Name",
    "email": "Email",
    "id": "ID",
    "phone": "Phone",
    "role": "Role",
}


def read_input_data(input_file) -> pd.DataFrame:
    if path.exists(input_file):
        df = pd.read_excel(input_file)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), input_file)

    return df


file_names = []


def generate_qr_codes(data, idx):
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
    img.save(path.join(IMAGES_PATH, f"qr{str(idx)}.png"))
    file_names.append(f"qr{str(idx)}.png")


def retrieve_data(df: pd.DataFrame) -> None:
    if not path.exists(IMAGES_PATH):
        os.mkdir(IMAGES_PATH)
    attributes = list(HEADERS.values())
    for row in range(len(df.index)):
        attendee_data = "".join(
            str(df.iloc[row, attr]) + "\n" for attr in range(len(df.columns))
        )

        generate_qr_codes(attendee_data, row)


def upload_qr_code_to_drive(service, file_name):
		file_metadata = {"name": file_name}
		request_body = {"role": "reader", "type": "anyone"}
		mime_type = "image/png"
		media = MediaFileUpload(path.join(IMAGES_PATH, "{0}").format(file_name), mimetype=mime_type)
		
		file = (
		    service.files()
		    .create(body=file_metadata, media_body=media, fields="webViewLink")
		    .execute()
		)

		qr_code_link = file.get("webViewLink")
		qr_code_id = qr_code_link.split("/")[-2]

		response_permission = (
        service.permissions()
        .create(fileId=qr_code_id, body=request_body)
        .execute()
    )
		
		response = {"qr_code_link":qr_code_link, "qr_code_id":qr_code_id}
		return response

qr_codes_ids = []
qr_codes_links = []
def get_qr_codes_urls(service):
		for file_name in file_names:

				try:
						response = upload_qr_code_to_drive(service, file_name)
				except HttpError as error:
						print(f"An error occurred: {error}")
						continue

				qr_codes_links.append(response.get("qr_code_link"))
				qr_codes_ids.append(response.get("qr_code_id"))

def insert_qr_codes(output_file: str, df: pd.DataFrame) -> None:
    links = pd.Series(qr_codes_links)
    ids = pd.Series(qr_codes_ids)
    df["QR_code"] = links
    df["QR_code_id"] = ids
    df.to_excel(output_file, index=False)

def main():
    parser = argparse.ArgumentParser(
        description="Generate QR codes for attendees and upload them to Google Drive"
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        help="Path to the input file. Default: attendees.csv",
        required=True,
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Path to the output file. Default: attendees_modified.xlsx",
        required=True,
    )
    args = parser.parse_args()

    ATTENDEES_XLSX_PATH = args.input
    df = read_input_data(ATTENDEES_XLSX_PATH)
    service = create_service()
    retrieve_data(df=df)
    get_qr_codes_urls(service)
    insert_qr_codes(output_file=args.output, df=df)


if __name__ == "__main__":
    main()

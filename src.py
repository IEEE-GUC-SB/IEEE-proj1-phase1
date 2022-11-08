from googleapiclient.http import MediaFileUpload
from googleservice import Create_Service
from googleapiclient.errors import HttpError
from os import path
import pandas as pd
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
import random
from faker import Faker
from faker.providers import internet

CLIENT_SECRET_FILE = 'credentials.json'
API_Name = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

def generate_dummy_data():
	if path.exists('./attendees.csv'):
		df = pd.read_csv('attendees.csv')
		return df
	elif path.exists('./attendees.xlsx'):
		read_file = pd.read_excel ("attendees.xlsx")
		read_file.to_csv ("attendees.csv", 
                  index = None,
                  header=True)
		df = pd.DataFrame(pd.read_csv("attendees.csv"))
		return df
	else:
		faker = Faker()
		df = pd.DataFrame(data = {})
		df.to_csv("./attendees.csv", sep=',',index=False)
		id_prefixes = ['L-', 'W-', 'HW-', 'SW-']
		names = []
		emails = []
		ids = []

		for _ in range(6):
			name = faker.name()
			id = f'{random.choice(id_prefixes)}{faker.random_number(digits = 5)}'
			first_name = name.split()[0].lower()
			last_name = name.split()[1].lower()
			email = f'{first_name}.{last_name}@{faker.free_email_domain()}'

			names.append(name)
			emails.append(email)
			ids.append(id)

	df['Name'] = names
	df['Email'] = emails
	df['ID'] = ids

	df.to_csv("./attendees.csv")
	return df

df = generate_dummy_data()

file_names = []
def qr_generating(data, idx):
	qr = qrcode.QRCode(version=5,error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=10,border=4,)
	qr.add_data(data)
	qr.make(fit = True)
	img = qr.make_image(image_factory=StyledPilImage, embeded_image_path="ieee_logo.png",module_drawer=RoundedModuleDrawer(), color_mask=RadialGradiantColorMask())
	img.save('qr' + str(idx) + '.png')
	file_names.append('qr' + str(idx) + '.png')



def retrieve_data():
	attributes = ['Name','Email','ID','Phone','Role']
	for row in range(0, len(df.index),1):
		attendee_data=''
		for attr in range(0,len(df.columns),1):
			attendee_data += str(df.iloc[row,attr])+'\n'
		qr_generating(attendee_data, row)


qr_codes_ids = []
def upload_to_drive():
	try:
		service = Create_Service(CLIENT_SECRET_FILE, API_Name, API_VERSION, SCOPES)

		for file_name in file_names:
			mime_type = 'image/png'
			file_metadata = {
				'name' : file_name
			}

			media = MediaFileUpload('./{0}'.format(file_name), mimetype=mime_type)
			file = service.files().create(
				body=file_metadata,
				media_body=media,
				fields='id'
			).execute()

			qr_codes_ids.append(file.get("id"))

	except HttpError as error:
		print(F'An error occurred: {error}')
		


qr_codes_links = []
def get_qr_codes_urls():
	service = Create_Service(CLIENT_SECRET_FILE, API_Name, API_VERSION, SCOPES)
	for qr_code_id in qr_codes_ids:
		try:
			request_body = {
				'role' : 'reader',
				'type' : 'anyone'			
			}

			response_permission = service.permissions().create(fileId=qr_code_id, body=request_body).execute()

			response_shared_link = service.files().get(
				fileId=qr_code_id,
				fields='webViewLink'
			).execute()

			qr_codes_links.append(response_shared_link.get('webViewLink'))

		except HttpError as error:
			print(F'An error occurred: {error}')



def insert_qr_codes():
	links = pd.Series(qr_codes_links)
	ids = pd.Series(qr_codes_ids)
	df['QR_code'] = links
	df['QR_code_id'] = ids
	df.to_csv('attendees_modified.csv', index=False)
	df.to_excel("attendees_modified.xlsx") 



def main():
	retrieve_data()
	upload_to_drive()
	get_qr_codes_urls()
	insert_qr_codes()
 

if __name__=="__main__":
  main()

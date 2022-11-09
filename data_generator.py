import random
import pandas as pd
from faker import Faker
from faker.providers import internet

faker = Faker()

def generate_dummy_data():
	df = pd.DataFrame(data = {})
	df.Name = "attendees.csv"
	df.to_csv(df.Name, sep=',',index=False)
	id_prefixes = ['L-', 'W-', 'HW-', 'SW-']
	names = []
	emails = []
	ids = []

	num_of_rows = int(input("Number of rows? \n"))

	for _ in range(num_of_rows):
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
	print(num_of_rows, ' rows generated in ', df.Name)
	return df
import random
import pandas as pd
from faker import Faker
from faker.providers import internet

faker = Faker()

df = pd.DataFrame(data = {})
df.Name = "attendees.csv"
df.to_csv(df.Name, sep=',',index=False)
id_prefixes = ['L-', 'W', 'HW-', 'SW-']
names = []
emails = []
ids = []

n = eval(input("Number of rows? \n"))

for _ in range(n):
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
print(n, ' rows generated in ', df.Name)
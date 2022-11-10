import argparse
import random

import pandas as pd
from faker import Faker

faker = Faker()


def generate_dummy_data(output_file: str, num_of_rows: int) -> None:
    df = pd.DataFrame(data={})
    id_prefixes = ["L-", "W-", "HW-", "SW-"]
    data = {
        "Names": [],
        "Emails": [],
        "Ids": [],
    }

    for _ in range(num_of_rows):
        name = faker.name()
        member_id = f"{random.choice(id_prefixes)}{faker.random_number(digits = 5)}"
        while member_id in data["Ids"]:
            member_id = f"{random.choice(id_prefixes)}{faker.random_number(digits = 5)}"
        first_name = name.split()[0].lower()
        last_name = name.split()[1].lower()
        email = f"{first_name}.{last_name}@{faker.free_email_domain()}"

        data["Names"].append(name)
        data["Emails"].append(email)
        data["Ids"].append(member_id)

    df = pd.DataFrame(data=data)

    df.to_excel(output_file, index=False, header=True, engine="xlsxwriter")
    print(f"Dummy data generated in {output_file} with {num_of_rows} rows")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--output", help="Output file name", required=True, type=str
    )
    parser.add_argument(
        "-n",
        "--num_of_rows",
        help="Number of rows",
        required=True,
        default=10,
        type=int,
    )
    args = parser.parse_args()
    generate_dummy_data(args.output, args.num_of_rows)


if __name__ == "__main__":
    main()

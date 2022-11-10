# attendees-qrcode

A Script that generates QR codes for attendees at an event. The script reads a csv or microsoft excel file containing the information of the attendees, generates a QR code encoding this information, and adds a new column containing links to the QR codes to the file. The QR codes are uploaded to google drive using an API request, then with another get request, the link of each QR code is fetched and added to its corresponding attendee's row in the sheet.

In order to run the script and make it upload the qr photos to a google drive, you can either:

1. Configure the Google Drive API yourself and download the credentials.json file, then add it to this folder. You can find instructions on how to configure the API online, or you can ask one of the contributors.

2. Contact one of the contributors to send you our own credentials file. It is not added here due to privacy concerns. You can find our emails in the Contributors section below.

### Installation

```bash
$ git clone https://github.com/IEEE-GUC-SB/IEEE-proj1-phase1
$ cd IEEE-proj1-phase1
```

The script requires `poetry` (a dependency management tool) to run. You can install `poetry` with pip as such:

```bash
$ pip3 install poetry
$ poetry install
```

### Usage

```bash
$ python3 generate_test_data.py -h
$ python3  --output <output_file> --num_of_rows <number_of_rows>
Dummy data generated in <output_file> with <number_of_rows> rows
$ python3 src.py -h
usage: src.py [-h] --input INPUT --output OUTPUT
$ python3 src.py --input <input_file> --output <output_file>
```

### Contributors

- [Amir Tarek](https://github.com/amir-awad) (amirtarek04@gmail.com)
- [Farida Maheeb](https://github.com/FaridaAbdelghaffar) (fmaheeb@gmail.com)
- [Omar Hesham](https://github.com/omarhesham02) (omar.hesham-youssef@outlook.com)

# attendees-qrcode

A Script that generates QR codes for attendees at an event. The script reads a csv or microsoft excel file containing the information of the attendees, generates a QR code encoding this information, and adds a new column containing links to the QR codes to the file. The QR codes are uploaded to google drive using an api request, then with another get request, the link of each QR code is fetched and added to its corresponding attendee's row in the sheet.

In order to run the script and make it upload the qr photos to a google drive, you can either:

1. Configure the Google Drive API yourself and download the credentials.json file, then add it to this folder. You can find instructions on how to configure the api online, or ask one of the contributors.

2. Contact one of the contributers to send you our own ready credentials file. It is not added here for privacy reasons. You can find our emails in the Contributors section below.


### Installation
The script requires ```poetry``` (a dependency management tool) to run. You can install ```poetry``` with pip as such:
```
$ pip3 install poetry
$ poetry install
```

### Usage

```
$ cd attendees-qrcode
$ python3 src.py
``` 
### Contributors
- [Amir Tarek](https://github.com/amir-awad) (amirtarek04@gmail.com)
- [Farida Maheeb](https://github.com/FaridaAbdelghaffar) (fmaheeb@gmail.com)
- [Omar Hesham](https://github.com/omarhesham02) (omar.hesham-youssef@outlook.com)

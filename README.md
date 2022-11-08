# attendees-qrcode

A Script that generates QR codes for attendees at an event. The script reads a csv or microsoft excel file containing the information of the attendees, generates a QR code encoding this information, and adds a new column containing links to the QR codes to the file. The QR codes are uploaded to google drive using an api request, then with another get request, the link of each QR code is fetched and added to its corresponding attendee's row in the sheet.

In order to run the script, you can either:

1. Delete the credentials file that exists in the project directory and configure the api youself, then use your own credentials (which takes much time).

2. You can be added as a test user by sending an email (containing your gmail email address) to one of the contributors. You can find our emails in the Contributors section.


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

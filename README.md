# attendees-qrcode

Script that generates QR codes for an event system attendees. The QR codes are uploaded to google drive using an api request, then with another get request the links of each QR code are fetched and added to their corresponding attendees rows in the sheet.

### Note: in order to run the script, you have two options: The first is to delete the credentials file that exists in the project directory and configure the api youself, then use your own credentials (which takes much time). The second one is to be added as a test user by sending your email to one of the contributers (e.g amirawad004@gmail.com)

### Installation
```
$ pip3 install poetry
$ poetry install
```

### Usage
```
$ cd attendees-qrcode
$ python3 src.py
``` 
### Contributers
- [Amir Tarek](https://github.com/amir-awad)
- [Farida Maheeb](https://github.com/FaridaAbdelghaffar)
- [Omar Hesham](https://github.com/omarhesham02)
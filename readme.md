# _Cowin Status Tracker_

These scripts allow you to view available vaccination slots for a pincode or district.
It can also notify about available slots through SMS (optional).

### Usage

`python district.py districtname [--sms]`

OR

`python pincode.py pincode [--sms]`

Note:

* For *nix systems, replace `python` with `python3`.

* If the district name has multiple words, it needs to be written as "district name" (for Windows) or 'district name' (for *nix). Otherwise " " or ' ' are optional.

    For Windows:
    `python district.py "East Delhi"`

    For *nix:
    `python3 district.py 'East Delhi'`

* `--sms` is optional. Use this flag to enable sms notifications.

These script will fetch status automatically every 5 minutes and display it on terminal. To exit the script, just press `Ctrl + C`.

### Enabling SMS Notifications (Optional)

1. Create a [Twilio Account](https://www.twilio.com/)
2. Login to your account and get a trial phone number.
3. Get ACCOUNT SID, AUTH TOKEN and PHONE NUMBER from [Twilio Console](https://www.twilio.com/console)
4. Create a new file `secrets.env` and paste the info in this format:
```
accountSID = your-account-sid
authToken = your-auth-token
myTwilioNumber = your-twilio-generated-phone-number
destNumber = your-personal-registered-number-with-country-code
```
SMS will be sent to your registered phone number if `--sms` flag is set and slots are available.

### Dependency
These script use some external libraries which can be installed using pip.

For Windows:
`pip install -r requirements.txt`

For *nix:
`pip3 install -r requirements.txt`

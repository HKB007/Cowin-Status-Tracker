from datetime import date
from os import getenv
from time import sleep

import requests
from dotenv import load_dotenv
from twilio.rest import Client

TIMEOUT = 300

load_dotenv('secrets.env')
accountSid = getenv('accountSID')
authToken = getenv('authToken')
myTwilioNumber = getenv('myTwilioNumber')
destCellPhone = getenv('destNumber')
twilioClient = Client(accountSid, authToken)


def scan(home, params, sendmsg=False):
    try:
        while True:
            try:
                params['date'] = date.today().strftime('%d-%m-%y')

                r = requests.get(home, params=params)
                js = r.json()
                centers = js['centers']

                msg = ''
                for center in centers:
                    for session in center['sessions']:
                        if session['min_age_limit'] == 18 and session['available_capacity'] > 0:
                            msg += f"{session['available_capacity']} {session['vaccine']} vaccines available in {center['name']} ({center['pincode']}) on {session['date']}\n"

                if msg:
                    print(msg)
                    if sendmsg:
                        send_message(msg)
                else:
                    print('No vaccination session found')

                print(f'Sleeping for {TIMEOUT} seconds...')
                sleep(TIMEOUT)

            except KeyboardInterrupt:
                raise KeyboardInterrupt()

            except:
                print(f'ERROR: Invalid PIN Code / Request Limit Reached')
                print(f'Sleeping for {TIMEOUT} seconds...\n')
                sleep(TIMEOUT)

    except KeyboardInterrupt:
        print('Exiting...')


def send_message(msg):
    twilioClient.messages.create(body=msg, from_=myTwilioNumber, to=destCellPhone)

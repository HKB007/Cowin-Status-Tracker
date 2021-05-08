from datetime import date
from os import getenv
from sys import exit
from time import sleep

import requests
from dotenv import load_dotenv
from plyer import notification
from twilio.rest import Client

TIMEOUT = 300
twilioClient = None


def scan(home, params, sendmsg=False):
    if sendmsg:
        load_dotenv('secrets.env')
        accountSid = getenv('accountSID')
        authToken = getenv('authToken')
        myTwilioNumber = getenv('myTwilioNumber')
        destNumber = getenv('destNumber')

        if not accountSid or not authToken or not myTwilioNumber or not destNumber:
            print('Invalid "secrets.env". Please verify and try again.')
            exit(1)

        global twilioClient
        twilioClient = Client(accountSid, authToken)

    try:
        while True:
            try:
                params['date'] = date.today().strftime('%d-%m-%y')

                user_agent = {'User-Agent': 'Mozilla/5.0'}
                r = requests.get(home, params=params, headers=user_agent)
                js = r.json()
                centers = js['centers']

                msg = ''
                for center in centers:
                    for session in center['sessions']:
                        if session['min_age_limit'] == 18 and session['available_capacity'] > 0:
                            msg += f"{session['available_capacity']} {session['vaccine']} vaccines available in {center['name']} ({center['pincode']}) on {session['date']}\n"

                if msg:
                    print(msg)
                    toastNotify(
                        'Some vaccination slots found.\nCheck terminal window and Cowin website.')
                    if sendmsg:
                        send_message(msg, myTwilioNumber, destNumber)
                else:
                    print('No vaccination session found')

                print(f'Sleeping for {TIMEOUT} seconds...')
                sleep(TIMEOUT)

            except KeyboardInterrupt:
                raise KeyboardInterrupt()

            except:
                print(f'ERROR: Invalid PIN Code / District Name / Request Limit Reached')
                print(f'Sleeping for {TIMEOUT} seconds...')
                sleep(TIMEOUT)

    except KeyboardInterrupt:
        print('\nExiting...')


def send_message(msg, sender, receiver):
    twilioClient.messages.create(body=msg, from_=sender, to=receiver)


def toastNotify(msg):
    notification.notify(title='Cowin Status Tracker', message=msg, timeout=0)

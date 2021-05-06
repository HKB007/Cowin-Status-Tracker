from datetime import date
from sys import argv
from time import sleep

import requests

PINCODE = argv[1]
TIMEOUT = 600
HOME = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin'
params = {'pincode': PINCODE}

try:
    while True:
        try:
            params['date'] = date.today().strftime('%d-%m-%y')

            r = requests.get(HOME, params=params)
            js = r.json()
            centers = js['centers']

            flag = False
            for center in centers:
                for session in center['sessions']:
                    if session['min_age_limit'] == 18 and session['available_capacity'] > 0:
                        print(
                            f"{session['available_capacity']} {session['vaccine']} vaccines available in {center['name']} ({center['pincode']}) on {session['date']}")
                        flag = True

            if not flag:
                print('No vaccination session found')

            print(f'Sleeping for {TIMEOUT} seconds...\n')
            sleep(TIMEOUT)

        except KeyboardInterrupt:
            raise KeyboardInterrupt()

        except:
            print('Some error occured')
            print(f'Sleeping for {TIMEOUT} seconds...')
            sleep(TIMEOUT)

except KeyboardInterrupt:
    print('Exiting...')

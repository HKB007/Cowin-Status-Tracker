from datetime import date
from sys import argv, exit
from time import sleep
import json

import requests

with open('dist_map.json', 'r', encoding='utf8') as fp:
    MAP = json.load(fp)
    
DISTRICT = argv[1]
DIST_ID = MAP.get(DISTRICT.lower(), None)
TIMEOUT = 600
HOME = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'

if DIST_ID is None:
    print('Invalid District Name... Please cross check from dist_map.json')
    exit(0)

params = {'district_id': DIST_ID}

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

            print(f'Sleeping for {TIMEOUT} seconds...')
            sleep(TIMEOUT)

        except KeyboardInterrupt:
            raise KeyboardInterrupt()

        except:
            print('Some error occured')
            print(f'Sleeping for {TIMEOUT} seconds...\n')
            sleep(TIMEOUT)

except KeyboardInterrupt:
    print('Exiting...')

from datetime import date
from time import sleep

import requests
from plyer import notification

TIMEOUT = 60
twilioClient = None


def scan(home, get_params, **kwargs):
    age = kwargs["age"]
    dose_no = kwargs["dose_no"]
    vacname = kwargs["vacname"]
    sendmsg = kwargs["sendmsg"]

    if sendmsg:
        from os import getenv

        from dotenv import load_dotenv
        from twilio.rest import Client

        load_dotenv("secrets.env")
        accountSid = getenv("accountSID")
        authToken = getenv("authToken")
        myTwilioNumber = getenv("myTwilioNumber")
        destNumber = getenv("destNumber")

        if not accountSid or not authToken or not myTwilioNumber or not destNumber:
            print('Invalid "secrets.env". Please verify and try again.')
            return

        global twilioClient
        twilioClient = Client(accountSid, authToken)

    try:
        while True:
            try:
                get_params["date"] = date.today().strftime("%d-%m-%y")
                user_agent = {"User-Agent": "Mozilla/5.0"}
                r = requests.get(home, params=get_params, headers=user_agent)
                js = r.json()
                centers = js["centers"]

                msg = ""
                for center in centers:
                    for session in center["sessions"]:
                        if (
                            session["min_age_limit"] <= age
                            and session["available_capacity"] > 0
                            and vacname.lower() in session["vaccine"].lower()
                        ):
                            dose1 = (
                                session["available_capacity_dose1"]
                                if dose_no == 1 or dose_no is None
                                else 0
                            )
                            dose2 = (
                                session["available_capacity_dose2"]
                                if dose_no == 2 or dose_no is None
                                else 0
                            )

                            if dose1 > 0 and dose2 > 0:
                                dosestr = "dose 1+2"
                            elif dose1 > 0:
                                dosestr = "dose 1"
                            elif dose2 > 0:
                                dosestr = "dose 2"
                            else:
                                continue
                            msg += f"{dose1 + dose2} {session['vaccine']} vaccines ({dosestr}) available for age >= {session['min_age_limit']} in {center['name']} ({center['pincode']}) on {session['date']}\n"

                if msg:
                    print(msg)
                    toastNotify(
                        "Some vaccination slots found.\nCheck terminal window and Cowin website."
                    )
                    if sendmsg:
                        send_message(msg, myTwilioNumber, destNumber)
                else:
                    print("No vaccination session found")

                print(f"Sleeping for {TIMEOUT} seconds...")
                sleep(TIMEOUT)

            except KeyboardInterrupt:
                raise KeyboardInterrupt()

            except:
                print(f"ERROR: Request Limit Reached / Network Error")
                print(f"Sleeping for {TIMEOUT} seconds...")
                sleep(TIMEOUT)

    except KeyboardInterrupt:
        print("\nExiting...")


def send_message(msg, sender, receiver):
    twilioClient.messages.create(body=msg, from_=sender, to=receiver)


def toastNotify(msg):
    notification.notify(title="Cowin Status Tracker", message=msg, timeout=0)

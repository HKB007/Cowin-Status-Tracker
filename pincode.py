from argparse import ArgumentParser

from util import scan


def parseArguments():
    parser = ArgumentParser(allow_abbrev=False)
    parser.add_argument('pincode', type=int, help='Pincode to search for')
    parser.add_argument('-age', metavar='yourage', type=int,
                        required=False, default=float('inf'), help='Your age')
    parser.add_argument('-dose', metavar='dosenumber', type=int,
                        required=False, default=None, help='Dose Number')
    parser.add_argument('-v', metavar='vaccinename', type=str,
                        required=False, default='', help='Vaccine Name')
    parser.add_argument('--sms', required=False, action='store_true',
                        help='Use this flag to enable sms alerts')
    return parser.parse_args()


def main():
    args = parseArguments()
    PINCODE = args.pincode
    AGE = args.age
    DOSE_NO = args.dose
    VACCINE_NAME = args.v
    SMS_ENABLE = args.sms

    HOME = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin'

    get_params = {'pincode': PINCODE}
    scan(HOME, get_params, age=AGE, dose_no=DOSE_NO, vacname=VACCINE_NAME, sendmsg=SMS_ENABLE)


if __name__ == '__main__':
    main()

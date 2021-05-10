from argparse import ArgumentParser
import json

from util import scan


def parseArguments():
    parser = ArgumentParser(allow_abbrev=False)
    parser.add_argument('statename', type=str,
                        help='State of your district')
    parser.add_argument('districtname', type=str,
                        help='District name to search for')
    parser.add_argument('-age', metavar='yourage', type=int,
                        required=False, default=float('inf'), help='Your age')
    parser.add_argument('--sms', required=False, action='store_true',
                        help='Use this flag to enable sms alerts')
    return parser.parse_args()


def main():
    args = parseArguments()
    STATE = args.statename
    DISTRICT = args.districtname
    SMS_ENABLE = args.sms
    AGE = args.age

    with open('dist_map.json', 'r', encoding='utf8') as fp:
        MAP = json.load(fp)

    st = MAP.get(STATE.lower(), None)
    if st is None:
        print('Invalid State Name... Please cross check from dist_map.json')
        return

    dist_id = st.get(DISTRICT.lower(), None)
    if dist_id is None:
        print('Invalid District Name... Please cross check from dist_map.json')
        return

    HOME = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'

    params = {'district_id': dist_id}
    scan(HOME, params, age=AGE, sendmsg=SMS_ENABLE)


if __name__ == '__main__':
    main()

from argparse import ArgumentParser
import json
from sys import exit

from util import scan


def parseArguments():
    parser = ArgumentParser(allow_abbrev=False)
    parser.add_argument('districtname', type=str,
                        help='District name to search for')
    parser.add_argument('--sms', required=False, action='store_true',
                        help='Use this flag to enable sms alerts')
    return parser.parse_args()


def main():
    args = parseArguments()
    DISTRICT = args.districtname
    SMS_ENABLE = args.sms

    with open('dist_map.json', 'r', encoding='utf8') as fp:
        MAP = json.load(fp)

    DIST_ID = MAP.get(DISTRICT.lower(), None)
    if DIST_ID is None:
        print('Invalid District Name... Please cross check from dist_map.json')
        exit(1)

    HOME = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'

    params = {'district_id': DIST_ID}
    scan(HOME, params, sendmsg=SMS_ENABLE)


if __name__ == '__main__':
    main()

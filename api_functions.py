import requests
import constants
import json
import sys


# documentation at http://developer.oanda.com/rest-live-v20/introduction/
# TODO solve possible exceptions in functions
# TODO add short positions


def get_price(instrument='EUR_USD', count=1):
    url = 'https://{}/v3/instruments/{}/candles'.format(constants.HOSTNAME, instrument)
    header = {'Authorization': 'Bearer {}'.format(constants.TOKEN)}
    query = {'price': 'BA', 'count': count}

    req = requests.get(url=url, headers=header, params=query)
    # json.dump(req.json(), sys.stdout, indent=2)

    return req.json()['candles'][0]['ask']['o'], req.json()['candles'][0]['bid']['o']


# buying
def open_long(units, instrument='EUR_USD'):
    url = 'https://{}/v3/accounts/{}/orders'.format(constants.HOSTNAME, constants.ACCOUNT_ID)
    header = {'Authorization': 'Bearer {}'.format(constants.TOKEN),
              'Content-Type': 'application/json'}
    body = {'order': {'type': 'MARKET', 'units': units, 'instrument': instrument}}

    body_json = json.JSONEncoder().encode(body)

    req = requests.post(url=url, headers=header, data=body_json)
    # json.dump(req.json(), sys.stdout, indent=2)


def close_long(instrument='EUR_USD'):
    url = 'https://{}/v3/accounts/{}/positions/{}/close'.format(constants.HOSTNAME, constants.ACCOUNT_ID, instrument)
    header = {'Authorization': 'Bearer {}'.format(constants.TOKEN),
              'Content-Type': 'application/json'}
    body = {'longUnits': 'ALL'}

    body_json = json.JSONEncoder().encode(body)

    req = requests.put(url=url, headers=header, data=body_json)
    # json.dump(req.json(), sys.stdout, indent=2)

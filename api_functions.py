import requests
import constants
import json
import sys


# documentation at http://developer.oanda.com/rest-live-v20/introduction/
# TODO add short positions


def get_price(instrument='EUR_USD', count=1):
    url = 'https://{}/v3/instruments/{}/candles'.format(constants.HOSTNAME, instrument)
    header = {'Authorization': 'Bearer {}'.format(constants.TOKEN)}
    query = {'price': 'BA', 'count': count}
    res = False

    try:
        res = requests.get(url=url, headers=header, params=query)
        # json.dump(res.json(), sys.stdout, indent=2)
    except Exception as e:
        print(e)

    if res:
        return res.json()['candles'][0]['ask']['o'], res.json()['candles'][0]['bid']['o']
    else:
        return None, None


# buying
# TODO solve possible exceptions
def open_long(units, instrument='EUR_USD'):
    url = 'https://{}/v3/accounts/{}/orders'.format(constants.HOSTNAME, constants.ACCOUNT_ID)
    header = {'Authorization': 'Bearer {}'.format(constants.TOKEN),
              'Content-Type': 'application/json'}
    body = {'order': {'type': 'MARKET', 'units': units, 'instrument': instrument}}

    body_json = json.JSONEncoder().encode(body)

    res = requests.post(url=url, headers=header, data=body_json)
    # json.dump(res.json(), sys.stdout, indent=2)


def close_long(instrument='EUR_USD'):
    url = 'https://{}/v3/accounts/{}/positions/{}/close'.format(constants.HOSTNAME, constants.ACCOUNT_ID, instrument)
    header = {'Authorization': 'Bearer {}'.format(constants.TOKEN),
              'Content-Type': 'application/json'}
    body = {'longUnits': 'ALL'}

    body_json = json.JSONEncoder().encode(body)

    res = requests.put(url=url, headers=header, data=body_json)
    # json.dump(res.json(), sys.stdout, indent=2)

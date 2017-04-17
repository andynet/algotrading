import requests
import json
import constants
import sys

# documentation at http://developer.oanda.com/rest-live-v20/introduction/

url = 'https://{}/v3/accounts/{}/orders'.format(constants.HOSTNAME, constants.ACCOUNT_ID)

header = {'Content-Type': 'application/json',
          'Authorization': 'Bearer {}'.format(constants.TOKEN)}

body = {'order': ({'instrument': 'EUR_USD', 'units': 100, 'type': 'MARKET'})}

json1 = json.JSONEncoder().encode(body)
# json.dump(json1, sys.stdout, indent=2)

r = requests.post(url, data=json1, headers=header)
json.dump(r.json(), sys.stdout, indent=2)

r = requests.get(url, headers=header)
# json.dump(r.json(), sys.stdout, sort_keys=True, indent=2)

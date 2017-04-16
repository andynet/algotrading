import v20
import constants
import functions
import time

print(constants.HOSTNAME, constants.TOKEN, constants.ACCOUNT_ID)

api = v20.Context(hostname=constants.HOSTNAME, token=constants.TOKEN)
account = api.account.get(accountID=constants.ACCOUNT_ID)
# response = api.order.market(constants.ACCOUNT_ID, instrument='EUR_USD', units=100)

while True:

    response = api.pricing.get(constants.ACCOUNT_ID, instruments='EUR_USD')
    # print(response)

    for price in response.get("prices", 200):
        print("Buy at", price.bids[0].price)

    time.sleep(1)

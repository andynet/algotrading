import time
import api_functions

while True:
    buy_price, sell_price = api_functions.get_price()
    line = buy_price + ' ' + sell_price + '\n'

    with open('EUR_USD.collected', 'a') as f:
        f.write(line)

    time.sleep(5)

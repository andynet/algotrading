import time
import api_functions

# TODO add time to records?
# TODO write output file format specification

while True:
    buy_price, sell_price = api_functions.get_price()
    line = buy_price + ' ' + sell_price + '\n'

    with open('EUR_USD.collected', 'a') as f:
        f.write(line)

    time.sleep(5)

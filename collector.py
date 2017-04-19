import time
import api_functions

# TODO write output file format specification

try:
    while True:
        buy_price, sell_price = api_functions.get_price()
        line = str(buy_price) + ' ' + str(sell_price) + ' ' + time.ctime() + '\n'

        with open('EUR_USD.collected', 'a') as f:
            f.write(line)

        time.sleep(5)
except KeyboardInterrupt:
    print('interrupted')

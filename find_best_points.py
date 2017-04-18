import functions
import matplotlib.pyplot as plt
import numpy as np

buying_prices, selling_prices = functions.read_input("EUR_USD.collected")

buying_prices_local_min = functions.find_local_min_prices(buying_prices)
selling_prices_local_max = functions.find_local_max_prices(selling_prices)

realized_buy = [None]*len(buying_prices)
realized_sale = [None]*len(selling_prices)

in_position = False
balance = 1000

print(buying_prices_local_min)
print(selling_prices_local_max)

for i in range(len(buying_prices_local_min)):
    if buying_prices_local_min[i] is not None:
        if not in_position:
            position_buy_price = buying_prices_local_min[i]
            current_buypoint = i
            in_position = True
        if in_position and buying_prices_local_min[i] < position_buy_price:
            position_buy_price = buying_prices_local_min[i]
            current_buypoint = i
    if selling_prices_local_max[i] is not None:
        if in_position:
            current_sellpoint = i
            next_sellpoint = functions.find_next_sellpoint(current_sellpoint, selling_prices_local_max)
            next_buypoint = None

            if next_sellpoint is not None:
                next_buypoint = functions.find_next_buypoint(current_sellpoint, next_sellpoint,
                                                             selling_prices_local_max, buying_prices_local_min)

            if next_sellpoint is None and selling_prices_local_max[current_sellpoint] > position_buy_price:
                position_sell_price = selling_prices_local_max[current_sellpoint]
                balance = functions.realize_order(balance, current_buypoint, position_buy_price,
                                                  current_sellpoint, position_sell_price)

                realized_buy[current_buypoint+1] = position_buy_price
                realized_sale[current_sellpoint+1] = position_sell_price

                in_position = False

            if next_buypoint is not None and selling_prices_local_max[current_sellpoint] > position_buy_price:
                position_sell_price = selling_prices_local_max[current_sellpoint]
                balance = functions.realize_order(balance, current_buypoint, position_buy_price,
                                                  current_sellpoint, position_sell_price)

                realized_buy[current_buypoint + 1] = position_buy_price
                realized_sale[current_sellpoint + 1] = position_sell_price

                in_position = False

x = np.arange(len(buying_prices))
buying_prices = np.array(buying_prices).astype(np.double)
bpmask = np.isfinite(buying_prices)
selling_prices = np.array(selling_prices).astype(np.double)
spmask = np.isfinite(selling_prices)

plt.plot(x[bpmask], buying_prices[bpmask], "b-", label="buying prices")
plt.plot(x[spmask], selling_prices[spmask], "r-", label="selling price")
plt.plot(x, realized_buy, "bo")
plt.plot(x, realized_sale, "ro")
plt.legend()
plt.show()

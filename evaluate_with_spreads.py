import time

buying_prices = []
selling_prices = []

with open("EUR_USD.data") as f:
    lines = f.readlines()
    for line in lines:
        selling_prices.append(float(line.split()[0]))
        buying_prices.append(float(line.split()[1]))

# print(buying_prices)
# print(selling_prices)

order_placed = False
balance = 1000

for i in range(1, len(buying_prices) - 1):
    if buying_prices[i-1] > buying_prices[i] <= buying_prices[i+1] and not order_placed:
        order_buy = buying_prices[i]
        unit_amount = balance/order_buy
        order_placed = True
        print("balance/order_buy=unit_amount:", balance, "/", order_buy, "=", unit_amount)
    if selling_prices[i-1] < selling_prices[i] >= selling_prices[i+1] and order_placed and order_buy < selling_prices[i]:
        order_sell = selling_prices[i]
        balance = unit_amount*order_sell
        order_placed = False
        print("balance=order_sell*unit_amount:", balance, "=", order_sell, "*", unit_amount)
    if buying_prices[i] < order_buy and order_placed:
        better_order_buy = buying_prices[i]
        unit_amount = unit_amount*order_buy/better_order_buy
        order_buy = better_order_buy
        print("found better_order_buy:", order_buy, "unit_amount:", unit_amount)
    # not optimal... still does not solve sequence 1, 5, 4, 10 with spread 3

    time.sleep(1)
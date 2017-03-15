import functions

buying_prices, selling_prices = functions.read_input("EUR_USD.data")

buying_prices_local_min = functions.find_local_min(buying_prices)
selling_prices_local_max = functions.find_local_max(selling_prices)

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
                in_position = False

            if next_buypoint is not None and selling_prices_local_max[current_sellpoint] > position_buy_price:
                position_sell_price = selling_prices_local_max[current_sellpoint]
                balance = functions.realize_order(balance, current_buypoint, position_buy_price,
                                                  current_sellpoint, position_sell_price)
                in_position = False

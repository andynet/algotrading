def read_input(filename):
    buying_prices = []
    selling_prices = []

    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            buying_prices.append(float(line.split()[1]))
            selling_prices.append(float(line.split()[0]))

    return buying_prices, selling_prices


def find_local_min(prices):
    lokal_min_prices = []
    for i in range(1, len(prices) - 1):
        if prices[i - 1] > prices[i] <= prices[i + 1]:
            lokal_min_prices.append(prices[i])
        else:
            lokal_min_prices.append(None)

    return lokal_min_prices


def find_local_max(prices):
    lokal_max_prices = []
    for i in range(1, len(prices) - 1):
        if prices[i - 1] < prices[i] >= prices[i + 1]:
            lokal_max_prices.append(prices[i])
        else:
            lokal_max_prices.append(None)

    return lokal_max_prices


def find_next_sellpoint(current_sellpoint, selling_prices):
    current_sellpoint_value = selling_prices[current_sellpoint]
    for i in range(current_sellpoint, len(selling_prices)):
        if selling_prices[i] == None:
            continue
        if selling_prices[i] > current_sellpoint_value:
            return i

    return None


def find_next_buypoint(current_sellpoint, next_sellpoint, selling_prices, buying_prices):
    current_sellpoint_value = selling_prices[current_sellpoint]

    for i in range(current_sellpoint, next_sellpoint):
        if buying_prices[i] == None:
            continue
        if buying_prices[i] < current_sellpoint_value:
            return i

    return None

def realize_order(balance, buypoint, buypoint_value, sellpoint, sellpoint_value):
    text = 'buypoint = {:>10}, sellpoint = {:>10}'.format(buypoint, sellpoint)
    print(text)
    return balance/buypoint_value*sellpoint_value

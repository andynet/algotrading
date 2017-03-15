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
    for i in range(1, len(prices)-1):
        if prices[i-1] > prices[i] <= prices[i+1]:
            lokal_min_prices.append(prices[i])
        else:
            lokal_min_prices.append(None)

    return lokal_min_prices

def find_local_max(prices):
    lokal_max_prices = []
    for i in range(1, len(prices)-1):
        if prices[i-1] < prices[i] >= prices[i+1]:
            lokal_max_prices.append(prices[i])
        else:
            lokal_max_prices.append(None)

    return lokal_max_prices

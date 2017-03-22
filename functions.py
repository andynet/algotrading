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
    next_sellpoint_value = selling_prices[current_sellpoint]

    for i in range(current_sellpoint, next_sellpoint):
        if buying_prices[i] == None:
            continue
        if current_sellpoint_value > buying_prices[i] < next_sellpoint_value:
            return i

    return None

def realize_order(balance, buypoint, buypoint_value, sellpoint, sellpoint_value):
    text = 'Bought at price {} at buypoint {}, sold at price {} at sellpoint {}.'.format(buypoint_value, buypoint,
                                                                                        sellpoint_value, sellpoint)
    print(text, "Balance:", balance/buypoint_value*sellpoint_value)
    return balance/buypoint_value*sellpoint_value


def find_best_points(buying_prices, selling_prices):
    buying_prices_local_min = find_local_min(buying_prices)
    selling_prices_local_max = find_local_max(selling_prices)

    orders = [0] * len(buying_prices)
    in_position = False

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
                next_sellpoint = find_next_sellpoint(current_sellpoint, selling_prices_local_max)
                next_buypoint = None

                if next_sellpoint is not None:
                    next_buypoint = find_next_buypoint(current_sellpoint, next_sellpoint,
                                                       selling_prices_local_max, buying_prices_local_min)

                if next_sellpoint is None and selling_prices_local_max[current_sellpoint] > position_buy_price:
                    orders[current_buypoint + 1] = 1
                    orders[current_sellpoint + 1] = -1
                    in_position = False

                if next_buypoint is not None and selling_prices_local_max[current_sellpoint] > position_buy_price:
                    orders[current_buypoint + 1] = 1
                    orders[current_sellpoint + 1] = -1
                    in_position = False
    return orders


# # TODO change this function to return features specified in machine_learning.py, maybe delete this? :D
# def create_training_data(buying_prices, selling_prices, orders, start, end, max_step):
#     features = []
#     labels = []
#
#     for i in range(start, end):
#
#         if i <= max_step:
#             bp = buying_prices[0:i]
#             sp = selling_prices[0:i]
#             o = orders[i]
#         else:
#             bp = buying_prices[i-max_step:i]
#             sp = selling_prices[i-max_step:i]
#             o = orders[i]
#
#         current_price =
#         median =
#         minimum =
#         maximum =
#
#         feature = bp + sp
#         features.append(feature)
#         labels.append(o)
#
#     return features, labels

def get_stats(prices, xpoint, history):
    if xpoint < history:
        prices = prices[0:xpoint + 1]
    else:
        prices = prices[xpoint - history + 1:xpoint + 1]

    price = prices[-1]
    median = sorted(prices, key=float)[len(prices) // 2]
    minimum = min(prices)
    maximum = max(prices)

    result = [price, median, minimum, maximum]
    return result

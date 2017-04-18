def read_input(filename):
    buying_prices = []
    selling_prices = []

    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            buying_prices.append(float(line.split()[0]))
            selling_prices.append(float(line.split()[1]))

    return buying_prices, selling_prices


def find_local_min_prices(prices):
    local_min_prices = []
    for i in range(1, len(prices) - 1):
        if prices[i - 1] > prices[i] <= prices[i + 1]:
            local_min_prices.append(prices[i])
        else:
            local_min_prices.append(None)

    return local_min_prices


def find_local_max_prices(prices):
    local_max_prices = []
    for i in range(1, len(prices) - 1):
        if prices[i - 1] < prices[i] >= prices[i + 1]:
            local_max_prices.append(prices[i])
        else:
            local_max_prices.append(None)

    return local_max_prices


# TODO refactor from this line down
def find_next_sellpoint(current_sellpoint, selling_prices):
    current_sellpoint_value = selling_prices[current_sellpoint]
    for i in range(current_sellpoint, len(selling_prices)):
        if selling_prices[i] is None:
            continue
        if selling_prices[i] > current_sellpoint_value:
            return i

    return None


def find_next_buypoint(current_sellpoint, next_sellpoint, selling_prices, buying_prices):
    current_sellpoint_value = selling_prices[current_sellpoint]
    next_sellpoint_value = selling_prices[current_sellpoint]

    for i in range(current_sellpoint, next_sellpoint):
        if buying_prices[i] is None:
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
    buying_prices_local_min = find_local_min_prices(buying_prices)
    selling_prices_local_max = find_local_max_prices(selling_prices)

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


def convert_to_graph_values(points, buying_prices, selling_prices):
    values = []

    for i in range(len(points)):
        if points[i] == 0:
            values.append(None)
        if points[i] == 1:
            values.append(buying_prices[i])
        if points[i] == -1:
            values.append(selling_prices[i])

    return values

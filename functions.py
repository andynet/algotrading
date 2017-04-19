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


def find_next_selling_point(current_selling_point, selling_prices):
    current_selling_point_value = selling_prices[current_selling_point]
    for i in range(current_selling_point, len(selling_prices)):
        if selling_prices[i] is None:
            continue
        if selling_prices[i] > current_selling_point_value:
            return i

    return None


def find_next_buying_point(current_selling_point, next_selling_point, selling_prices, buying_prices):
    current_selling_point_value = selling_prices[current_selling_point]
    next_selling_point_value = selling_prices[current_selling_point]

    for i in range(current_selling_point, next_selling_point):
        if buying_prices[i] is None:
            continue
        if current_selling_point_value > buying_prices[i] < next_selling_point_value:
            return i

    return None


def realize_order(balance, buying_point, buying_point_value, selling_point, selling_point_value):
    text = 'Bought at price {} at buying point {}, sold at price {} at selling point {}.'.format(buying_point_value,
                                                                                                 buying_point,
                                                                                                 selling_point_value,
                                                                                                 selling_point)

    print(text, "Balance:", balance / buying_point_value * selling_point_value)
    return balance / buying_point_value * selling_point_value


def find_best_points(buying_prices, selling_prices):
    buying_prices_local_min = find_local_min_prices(buying_prices)
    selling_prices_local_max = find_local_max_prices(selling_prices)

    orders = [0] * len(buying_prices)
    in_position = False

    for i in range(len(buying_prices_local_min)):
        if buying_prices_local_min[i] is not None:
            if not in_position:
                position_buy_price = buying_prices_local_min[i]
                current_buying_point = i
                in_position = True
            if in_position and buying_prices_local_min[i] < position_buy_price:
                position_buy_price = buying_prices_local_min[i]
                current_buying_point = i
        if selling_prices_local_max[i] is not None:
            if in_position:
                current_selling_point = i
                next_selling_point = find_next_selling_point(current_selling_point, selling_prices_local_max)
                next_buying_point = None

                if next_selling_point is not None:
                    next_buying_point = find_next_buying_point(current_selling_point, next_selling_point,
                                                               selling_prices_local_max, buying_prices_local_min)

                if next_selling_point is None and selling_prices_local_max[current_selling_point] > position_buy_price:
                    orders[current_buying_point + 1] = 1
                    orders[current_selling_point + 1] = -1
                    in_position = False

                if next_buying_point is not None and selling_prices_local_max[
                    current_selling_point] > position_buy_price:
                    orders[current_buying_point + 1] = 1
                    orders[current_selling_point + 1] = -1
                    in_position = False
    return orders


def get_stats(prices, x_point, history):
    if x_point < history:
        prices = prices[0:x_point + 1]
    else:
        prices = prices[x_point - history + 1:x_point + 1]

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

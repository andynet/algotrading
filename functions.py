def read_input(filename):
    buying_prices = []
    selling_prices = []

    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            buying_prices.append(float(line.split()[0]))
            selling_prices.append(float(line.split()[1]))

    return buying_prices, selling_prices


def create_labels(buying_points, selling_points):
    labels = []
    last_buying_point = None
    last_selling_point = None

    for i in range(len(buying_points)):
        labels.append(0)
        if buying_points[i] == 1:
            labels[i] = 1
            last_buying_point = i
            if last_selling_point is not None:
                for j in range(last_selling_point + 1, last_buying_point):
                    labels[j] = 4
        if selling_points[i] == 1:
            labels[i] = 3
            last_selling_point = i
            if last_buying_point is not None:
                for j in range(last_buying_point + 1, last_selling_point):
                    labels[j] = 2

    return labels


def evaluate(starting_balance, buying_prices, selling_prices, buying_points, selling_points):
    buying_price = None
    selling_price = None
    balance = starting_balance

    for i in range(len(buying_prices)):
        if buying_points[i] == 1 and selling_price is None:
            buying_price = buying_prices[i]
        if selling_points[i] == 1 and buying_price is not None:
            selling_price = selling_prices[i]
            balance = balance / buying_price * selling_price
            buying_price = None
            selling_price = None

    return balance


def draw_plot(buying_prices, selling_prices, buying_points, selling_points):
    import matplotlib.pyplot as plt
    for i in range(len(buying_points)):
        buying_points[i] = buying_points[i] * buying_prices[i]
        selling_points[i] = selling_points[i] * selling_prices[i]
        if buying_points[i] == 0:
            buying_points[i] = None
        if selling_points[i] == 0:
            selling_points[i] = None

    plt.plot(buying_prices, "b-", label="buying prices")
    plt.plot(selling_prices, "r-", label="selling price")
    plt.plot(buying_points, "bo")
    plt.plot(selling_points, "ro")
    plt.legend()
    plt.show()


def create_features(buying_prices, selling_prices, buying_points, selling_points, number=7):
    # actual buying price, actual selling price,
    # number of time units from last start of cycle, number of time units from last end of cycle
    # value of last optimal buying point, value of last optimal selling point
    # average of prices from last buying point, average of prices from last selling point
    # average of prices of last _integer_ buying points, average of prices of last _integer_ selling points
    # average of durations of last _integer_ positive cycles, average of durations of last _integer_ negative cycles

    from_last_buy, from_last_sell = None, None
    last_optimal_buy, last_optimal_sell = None, None
    average_from_last_buy, average_from_last_sell = None, None
    average_buying_prices, average_selling_prices = None, None
    average_buying_duration, average_selling_duration = None, None

    features = []
    buying_points_positions = []
    selling_points_positions = []

    for i in range(len(buying_prices)):

        buying_price = buying_prices[i]
        selling_price = selling_prices[i]

        if buying_points[i] == 1:
            buying_points_positions.append(i)

        if selling_points[i] == 1:
            selling_points_positions.append(i)

        if len(buying_points_positions) > 0:
            from_last_buy = i - buying_points_positions[-1]
            last_optimal_buy = buying_prices[buying_points_positions[-1]]
            average_from_last_buy = sum(buying_prices[buying_points_positions[-1]:(i + 1)]) / (from_last_buy + 1)

        if len(selling_points_positions) > 0:
            from_last_sell = i - selling_points_positions[-1]
            last_optimal_sell = selling_prices[selling_points_positions[-1]]
            average_from_last_sell = sum(selling_prices[selling_points_positions[-1]:(i + 1)]) / (from_last_sell + 1)

        if len(buying_points_positions) >= (number + 1):
            average_buying_prices = 0
            average_buying_duration = 0
            for j in range(number):
                average_buying_prices += buying_prices[buying_points_positions[-(1 + j)]]
                average_buying_duration += buying_points_positions[-(1 + j)] - buying_points_positions[-(2 + j)]
            average_buying_prices /= number
            average_buying_duration /= number

        if len(selling_points_positions) >= (number + 1):
            average_selling_prices = 0
            average_selling_duration = 0
            for j in range(number):
                average_selling_prices += selling_prices[selling_points_positions[-(1 + j)]]
                average_selling_duration += selling_points_positions[-(1 + j)] - selling_points_positions[-(2 + j)]
            average_selling_prices /= number
            average_selling_duration /= number

        result = [buying_price, selling_price,
                  from_last_buy, from_last_sell,
                  last_optimal_buy, last_optimal_sell,
                  average_from_last_buy, average_from_last_sell,
                  average_buying_prices, average_selling_prices,
                  average_buying_duration, average_selling_duration]

        features.append(result)

    return features


def filter(labels, features):
    used_from = 0
    used_to = 0
    contain_useful_data = False

    for i in range(len(labels)):
        if not contain_useful_data:
            if features[i][11] is None or features[i][10] is None:
                used_from = i
            else:
                used_from += 1
                contain_useful_data = True

        if contain_useful_data:
            if features[i][11] is not None and features[i][10] is not None:
                used_to = i
            else:
                break

    return used_from, used_to

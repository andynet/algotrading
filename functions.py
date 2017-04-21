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

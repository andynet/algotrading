def read_input(filename):
    buying_prices = []
    selling_prices = []

    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            buying_prices.append(float(line.split()[0]))
            selling_prices.append(float(line.split()[1]))

    return buying_prices, selling_prices


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

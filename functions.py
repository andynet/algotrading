def read_input(filename):
    buying_prices = []
    selling_prices = []

    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            buying_prices.append(float(line.split()[1]))
            selling_prices.append(float(line.split()[0]))

    return buying_prices, selling_prices
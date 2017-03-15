import functions
import sklearn

buying_prices, selling_prices = functions.read_input("EUR_USD.data")
orders = functions.find_best_points(buying_prices, selling_prices)

for i in range(50, len(buying_prices))
    features = buying_prices

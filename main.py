import sklearn
from classes import *

buying_prices = []
selling_prices = []

# features = array of numbers:
# actual buying price, actual selling price,
# number of time units from last start of cycle, number of time units from last end of cycle
# value of last optimal buying point, value of last optimal selling point
# average of prices from last buying point, average of prices from last selling point
# average of prices of last _integer_ buying points, average of prices of last _integer_ selling points
# average of durations of last _integer_ positive cycles, average of durations of last _integer_ negative cycles
features = []
predictions = []

order = Order()
feeder = Feeder('EUR_USD.collected.2604')  # should be name of file or keyword 'online'
investigator = Investigator()
# evaluator = Evaluator()

while True:
    buying_price, selling_price = feeder.get_prices()

    if buying_price is None or selling_price is None:
        break

    buying_prices.append(buying_price)
    selling_prices.append(selling_price)

    buying_points, selling_points = investigator.examine(buying_price, selling_price)

    # labels = functions.create_labels(buying_points, selling_points)
    # features = functions.create_features(buying_prices, selling_prices, buying_points, selling_points, 7)

    #
    # features.append(feature)

    # used_from = filter_from()
    # used_to = filter_to()
    #
    # clf = sklearn.tree.DecisionTreeClassifier()
    # clf.fit(features[used_from:used_to], labels[used_from:used_to])
    # prediction = clf.predict([features[-1]])
    #
    # predictions.append(prediction)
    #
    # if prediction == 1 and not order.exists():
    #     api_functions.open_long(balance)
    #     order.create()
    #
    # if prediction == 3 and order.exists():
    #     api_functions.close_long()
    #     order.close()

buying_points, selling_points = investigator.get_results()
# labels = functions.create_labels(buying_points, selling_points)
# print(labels)
features = functions.create_features(buying_prices[0:100], selling_prices[0:100],
                                     buying_points[0:100], selling_points[0:100], 7)
print(features[0:100], sep="\n")
best_case = functions.evaluate(100000, buying_prices, selling_prices, buying_points, selling_points)
# print(best_case)
# functions.draw_plot(buying_prices, selling_prices, buying_points, selling_points)

from sklearn.tree import DecisionTreeClassifier
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
# features = []
predictions = []

order = Order()
feeder = Feeder('EUR_USD.week18')  # should be name of file or keyword 'online'
investigator = Investigator()
features_creator = FeaturesCreator(7)
# evaluator = Evaluator()

balance = 100000
in_order = False
last_checked = -1
used_from = 0
used_to = 0

start = time.time()
while True:
    buying_price, selling_price = feeder.get_prices()

    if buying_price is None or selling_price is None:
        break

    buying_prices.append(buying_price)
    selling_prices.append(selling_price)

    buying_points, selling_points = investigator.examine(buying_price, selling_price)

    labels = functions.create_labels(buying_points, selling_points)  # TODO optimize
    features = features_creator.create_features(buying_prices, selling_prices,
                                                buying_points, selling_points)

    if used_from == 0:
        used_from, last_checked = functions.find_used_from(features, last_checked)

    if used_from != 0:
        used_to, last_checked = functions.find_used_to(labels, last_checked)

    if used_to - 1000 < used_from:
        begin = used_from
    else:
        begin = used_to - 1000

    if used_from < used_to:
        clf = DecisionTreeClassifier()
        used_features = features[begin:used_to]
        used_labels = labels[begin:used_to]
        # print(start - time.time())
        start = time.time()
        clf.fit(used_features, used_labels)
        prediction = clf.predict([features[-1]])

        predictions.append(prediction)

        # if prediction == 1 and not order.exists():
        # api_functions.open_long(balance)
        # order.create()
        if prediction == 1 and not in_order:
            balance = balance / buying_prices[-1]
            in_order = True

        # if prediction == 3 and order.exists():
        # api_functions.close_long()
        # balance = order.close()
        if prediction == 3 and in_order:
            balance = balance * selling_prices[-1]
            in_order = False

# buying_points, selling_points = investigator.get_results()

# start = time.time()
# labels = functions.create_labels(buying_points, selling_points)
# print(time.time() - start)
#
# start = time.time()
# features = functions.create_features(buying_prices, selling_prices,
#                                      buying_points, selling_points, 7)
# # print(features[0:100], sep="\n")
# print(time.time() - start)

best_case = functions.evaluate(100000, buying_prices, selling_prices, buying_points, selling_points)
print(best_case)
print(balance)
# functions.draw_plot(buying_prices, selling_prices, buying_points, selling_points)

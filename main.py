from sklearn.tree import DecisionTreeClassifier
from classes import *

# parameters
starting_balance = 1000  # positive integer
features_size = 1000  # positive integer, influences execution time
features_history = 7  # positive integer, influences execution time
input_dev = 'EUR_USD.week18'  # should be name of file or keyword 'online'

# classes initialization
feeder = Feeder(input_dev)
investigator = Investigator()
features_creator = FeaturesCreator(features_history)

# variables initialization
buying_prices = []
selling_prices = []
features = []
predictions = []
balance = starting_balance
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

    if used_to - features_size < used_from:
        begin = used_from
    else:
        begin = used_to - features_size

    if used_from < used_to:
        clf = DecisionTreeClassifier()
        used_features = features[begin:used_to]
        used_labels = labels[begin:used_to]
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

# start = time.time()
# features = functions.create_features(buying_prices, selling_prices,
#                                      buying_points, selling_points, 7)
# # print(features[0:100], sep="\n")
# print(time.time() - start)

best_case = functions.evaluate(starting_balance, buying_prices, selling_prices, buying_points, selling_points)
print(best_case)
print(balance)
# functions.draw_plot(buying_prices, selling_prices, buying_points, selling_points)

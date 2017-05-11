from sklearn.tree import DecisionTreeClassifier
from classes import *

# parameters
starting_balance = 1000  # positive integer
features_size = 1000  # positive integer, influences execution time
features_history = 7  # positive integer, influences execution time
input_dev = 'EUR_USD.week17'  # should be name of file or keyword 'online'

# classes initialization
feeder = Feeder(input_dev)
investigator = Investigator()
labels_creator = LabelsCreator()
features_creator = FeaturesCreator(features_history)
active_order = Order()

# variables initialization
buying_prices = []
selling_prices = []

# labels = []
# features = []

predictions = []
orders = []

balance = starting_balance
balance2 = starting_balance
invested = starting_balance

last_checked = -1
used_from = 0
used_to = 0

while True:

    start = time.time()

    buying_price, selling_price = feeder.get_prices()

    if buying_price is None or selling_price is None:
        break

    buying_prices.append(buying_price)
    selling_prices.append(selling_price)

    buying_points, selling_points = investigator.examine(buying_price, selling_price)

    labels = labels_creator.create_labels(buying_points, selling_points)
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

        trailing_stop = (features[-1][9] - features[-1][8]) * 0.2

        if prediction == 1:
            order = Order()
            order.create(buying_price, selling_price, invested, trailing_stop)
            orders.append(order)
            balance -= invested

        if len(orders) > 0:
            for order in orders:
                balance += order.check_trailing_stop(buying_price, selling_price)

        if prediction == 1 and not active_order.exists():
            active_order.create(buying_price, selling_price, invested, trailing_stop)
            balance2 = 0

        if active_order.exists():
            balance2 = active_order.check_trailing_stop(buying_price, selling_price)

    print(time.time() - start)

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
print(balance2)
# functions.draw_plot(buying_prices, selling_prices, buying_points, selling_points)

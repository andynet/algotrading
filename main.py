import sklearn
import functions
from BuyOrder import BuyOrder
import numpy as np
import matplotlib.pyplot as plt

buying_prices = []
selling_prices = []

# buying_points = []      # True or False
# selling_points = []     # True or False

# features = array of numbers:
# actual buying price, actual selling price,
# number of time units from last start of cycle, number of time units from last end of cycle
# value of last optimal buying point, value of last optimal selling point
# average of prices from last buying point, average of prices from last selling point
# average of prices of last _integer_ buying points, average of prices of last _integer_ selling points
# average of durations of last _integer_ positive cycles, average of durations of last _integer_ negative cycles
features = []

# labels = array of characters:
# B buy
# S sell
# U unidentified
# P positive trend
# N negative trend
labels = []
predictions = []

while True:
    buying_price, selling_price = functions.get_price("online")  # TODO create function get_price

    buying_prices.append(buying_price)
    selling_prices.append(selling_price)

    buying_points, selling_points = functions.get_best_points(buying_prices, selling_prices)

    features, labels = functions.get_statistics(buying_prices, selling_prices, buying_points, selling_points)
    identified_from, identified_to = functions.get_identified(labels)

    clf = sklearn.tree.DecisionTreeClassifier()
    clf.fit(features[identified_from:identified_to], labels[identified_from:identified_to])
    prediction = clf.predict([features[-1]])

    predictions.append(prediction)

    # if prediction == "B" and not BuyOrder.exists()

# labels = functions.convert_to_graph_values(labels, buying_prices, selling_prices)
# predictions = functions.convert_to_graph_values(predictions, buying_prices, selling_prices)
#
# x = np.arange(len(buying_prices))
# buying_prices = np.array(buying_prices).astype(np.double)
# bpmask = np.isfinite(buying_prices)
# selling_prices = np.array(selling_prices).astype(np.double)
# spmask = np.isfinite(selling_prices)
#
# plt.plot(x[bpmask], buying_prices[bpmask], "b-", label="buying prices")
# plt.plot(x[spmask], selling_prices[spmask], "r-", label="selling price")
# plt.plot(x, labels, "go", label="best_case")
# plt.plot(x, predictions, "yd", label="predictions")
# plt.legend()
# plt.show()

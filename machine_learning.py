from sklearn import tree
import v20
import const
import functions
import time

# api = v20.Context(hostname=const.HOSTNAME, token=const.TOKEN)
# account = api.account.get(accountID=const.ACCOUNT_ID)
# response = api.order.market(id, instrument='EUR_USD', units=100)

buying_prices, selling_prices = functions.read_input("EUR_USD_1000.data")
orders = functions.find_best_points(buying_prices, selling_prices)

# parameters for features
# - actual price
# - median of last n records
# - average of last n records   # for this version do not do average
# - min of last n records
# - max of last n records

training_start = 0
training_end = 100
training_record_size = 25
predictions = [0] * training_end  # for training data there should not be any predictions

features = []
labels = []

for i in range(training_start, training_end):
    buy_features = functions.get_stats(buying_prices, i, training_record_size)
    sell_features = functions.get_stats(selling_prices, i, training_record_size)

    features.append(buy_features + sell_features)
    labels.append(orders[i])

for i in range(training_end, len(orders)):
    buy_features = functions.get_stats(buying_prices, i, training_record_size)
    sell_features = functions.get_stats(selling_prices, i, training_record_size)

    feature = buy_features + sell_features

    clf = tree.DecisionTreeClassifier()
    clf.fit(features, labels)
    prediction = clf.predict([feature])
    label = orders[i]

    features.append(feature)
    labels.append(label)
    predictions.append(prediction)

    print("Prediction: {}\tLabel:{}".format(prediction, label))

print(len(predictions), len(orders))

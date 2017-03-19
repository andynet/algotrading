from sklearn import tree
import v20
import const
import functions

# api = v20.Context(hostname=const.HOSTNAME, token=const.TOKEN)
# account = api.account.get(accountID=const.ACCOUNT_ID)
# response = api.order.market(id, instrument='EUR_USD', units=100)

buying_prices, selling_prices = functions.read_input("EUR_USD.data")
orders = functions.find_best_points(buying_prices, selling_prices)

# create training data from datapoints <0,100), one feature will have 20 buying prices and 20 selling prices
features, labels = functions.create_training_data(buying_prices, selling_prices, orders, 0, 100, 20)
# predictions = []

for i in range(101, len(orders)):
    feature = buying_prices[i - 20:i] + selling_prices[i - 20:i]

    clf = tree.DecisionTreeClassifier()
    clf.fit(features, labels)
    prediction = clf.predict(feature)
    best_order = orders[i - 1]

    print("Prediction: {}\tBest order:{}".format(prediction, best_order))

    # to = 50
    #
    # feature = buying_prices[0:to]+selling_prices[0:to]
    # print(feature)
    # print(len(feature))
    # for i in range(to):
    #     print("{:>8}".format(buying_prices[i]), end=" ")
    #     print("{:>8}".format(selling_prices[i]), end=" ")
    #     print("{:>8}".format(orders[i]), end=" ")
    #     print(i)

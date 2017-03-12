import matplotlib.pyplot as plt

# class Order:
#
#     start_buy = 0
#     start_sell = 0
#     stop_buy = 0
#     stop_sell = 0
#     placed = False
#
#     def startOrder(self, start_buy, start_sell):
#         if not self.placed:
#             self.start_buy = start_buy
#             self.start_sell = start_sell
#             self.placed = True
#         else:
#             print("Error: Can not place order. One Order already placed.")
#
#     def stopOrder(self, stop_buy, stop_sell):
#         if self.placed:

buying_prices = []
selling_prices = []
balance = 1000

with open('./EUR_USD.data') as f:
    lines = f.readlines()

for line in lines:
    line = line.split()
    buying_prices.append(float(line[0]))
    selling_prices.append(float(line[1]))

buying_max = max(buying_prices)
selling_max = max(selling_prices)
buying_min = min(buying_prices)
selling_min = min(selling_prices)

x = range(0,len(buying_prices))
plt.plot(x, buying_prices, 'b-', x, selling_prices, 'r-')
plt.show()

for i in range(1, len(buying_prices)-1):
    if buying_prices[i-1] > buying_prices[i] <= buying_prices[i+1]:
        balance /= buying_prices[i]
    if selling_prices[i-1] < selling_prices[i] >= selling_prices[i+1]:
        balance *= selling_prices[i]

print(balance)
import matplotlib.pyplot as plt
import numpy as np

buying_prices = []
selling_prices = []
buying_prices_purified = []
selling_prices_purified = []

with open("EUR_USD.data") as f:
    lines = f.readlines()
    for line in lines:
        selling_prices.append(float(line.split()[0]))
        buying_prices.append(float(line.split()[1]))

for i in range(1, len(buying_prices)-1):
    if buying_prices[i-1] > buying_prices[i] <= buying_prices[i+1]:
        buying_prices_purified.append(buying_prices[i])
    else:
        buying_prices_purified.append(None)

    if selling_prices[i-1] < selling_prices[i] >= selling_prices[i+1]:
        selling_prices_purified.append(selling_prices[i])
    else:
        selling_prices_purified.append(None)

print(buying_prices_purified)
print(selling_prices_purified)

merged_prices = []
for i in range(0,len(buying_prices_purified)):
    if buying_prices_purified[i] != None and selling_prices_purified[i] != None:
        # print("Mam zly predpoklad")
        merged_prices.append(None)
    if buying_prices_purified[i] == None and selling_prices_purified[i] != None:
        merged_prices.append(selling_prices_purified[i])
    if buying_prices_purified[i] != None and selling_prices_purified[i] == None:
        merged_prices.append(buying_prices_purified[i])
    if buying_prices_purified[i] == None and selling_prices_purified[i] == None:
        merged_prices.append(None)

print(merged_prices)

xs = np.arange(max(len(buying_prices_purified), len(selling_prices_purified)))
series1 = np.array(buying_prices_purified).astype(np.double)
s1mask = np.isfinite(series1)
series2 = np.array(selling_prices_purified).astype(np.double)
s2mask = np.isfinite(series2)
series_merged = np.array(merged_prices).astype(np.double)
smmask = np.isfinite(series_merged)

plt.plot(xs[smmask], series_merged[smmask], "g-")
plt.plot(xs[s1mask], series1[s1mask], "bo", label="buying price")
plt.plot(xs[s2mask], series2[s2mask], "ro", label="selling price")
plt.legend()
plt.show()
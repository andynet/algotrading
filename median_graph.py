import functions
import numpy as np
import matplotlib.pyplot as plt

median_size = 50
buying_prices, selling_prices = functions.read_input("EUR_USD_1000.data")

buying_prices_median = [None] * (median_size - 1)
selling_prices_median = [None] * (median_size - 1)

for i in range(median_size, len(buying_prices)):
    bp = buying_prices[i - median_size:i]
    sp = selling_prices[i - median_size:i]

    # print(sorted(bp, key=float))
    # print(sorted(bp, key=float))

    bmedian = sum(sorted(bp, key=float)[24:26]) / 2
    smedian = sum(sorted(sp, key=float)[24:26]) / 2

    buying_prices_median.append(bmedian)
    selling_prices_median.append(smedian)

x = np.arange(len(buying_prices))
buying_prices = np.array(buying_prices).astype(np.double)
bpmask = np.isfinite(buying_prices)
# selling_prices = np.array(selling_prices).astype(np.double)
# spmask = np.isfinite(selling_prices)

buying_prices_median = np.array(buying_prices_median).astype(np.double)
bpm_mask = np.isfinite(buying_prices_median)
# selling_prices_median = np.array(selling_prices_median).astype(np.double)
# spm_mask = np.isfinite(selling_prices_median)


plt.plot(x[bpmask], buying_prices[bpmask], "b-", label="buying prices")
# plt.plot(x[spmask], selling_prices[spmask], "r-", label="selling price")
plt.plot(x[bpm_mask], buying_prices_median[bpm_mask], "c-")
# plt.plot(x[spm_mask], selling_prices_median[spm_mask], "m-")
plt.legend()
plt.show()

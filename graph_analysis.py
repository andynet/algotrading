
from random import randint

raw_prices = []
prices = []
lmin = 0
lmax = 0
good_balance = 100
bad_balance = 100
good_pos = False
bad_pos = False


with open('./EUR_USDv2', mode='r') as f:
    raw_prices = f.readlines()

prices.append(float('inf'))
for price in raw_prices:
    prices.append(float(price))
prices.append(float('-inf'))

for i in range(1, len(prices)-1):

    if prices[i-1] > prices[i] <= prices[i+1]:
        #print(str(prices[i]) + ' = minimum, treba kupit ' + str(i))

        good_balance = good_balance / prices[i]
        good_pos = True

        if bad_pos:
            bad_balance = bad_balance * prices[i]
            bad_pos = False

        lmin += 1

    if prices[i-1] <= prices[i] > prices[i+1]:
        #print(str(prices[i]) + ' = maximum, treba predat ' + str(i))

        if good_pos:
            good_balance = good_balance * prices[i]
            good_pos = False

        bad_balance = bad_balance / prices[i]
        bad_pos = True

        lmax += 1

nonext = len(prices)-2-lmin-lmax
#print(lmin, lmax, nonext)
print('long position, best case = ' + str(good_balance - 100))
print('long position, worst case = ' + str(bad_balance - 100))

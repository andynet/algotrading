# DEFINITION - cycle
# the time from one optimal buying point to next optimal buying point

# LIST - features for classifier
# - actual price
# - number of time units from last start of cycle
# - last optimal buying point
# - last optimal selling point
# - median of prices from last cycle
# - median of prices of last <integer> buying points    # <integer> = 7 (???)
# - median of prices of last <integer> selling points
# - median of durations of last <integer> cycles

# CLASS - BuyOrder
# order.exists()
# order.create(buy_price, sell_price, amount, trailing_stop)
# order.check_trailing_stop(buy_price, sell_price)
# order.close()

# PROPOSAL - trailing stop
# will be calculated as:
# (<median of prices of last <integer> selling points> - <median of prices of last <integer> buying points>) * 0.2 (???)
# this value will be subtracted from maximum already reached in this cycle
# if actual price will drop below, then order.close() will be called

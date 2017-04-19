# algotrading

DEFINITION - cycle
* the time from one optimal buying point to next optimal buying point

LIST - features for classifier
- actual buying price
- number of time units from last start of cycle
- last optimal buying point
- last optimal selling point
- average of prices from last buying point
- average of prices of last _integer_ buying points (_integer_ = 7 )
- average of prices of last _integer_ selling points
- average of durations of last _integer_ cycles

CLASS - BuyOrder
* order.exists()
* order.create(buy_price, sell_price, amount, trailing_stop)
* order.check_trailing_stop(buy_price, sell_price)
* order.close()

PROPOSAL - trailing stop
* will be calculated as:
* ((median of prices of last _integer_ selling points) - (median of prices of last _integer_ buying points)) * 0.2 (???)
* this value will be subtracted from maximum already reached in this cycle
* if actual price will drop below, then order.close() will be called

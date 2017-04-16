# finished - 17042017
class BuyOrder:
    active = False
    initial_buy_price = 0
    initial_sell_price = 0

    max_buy_price = 0
    trailing_stop = 0

    amount = 0

    def exists(self):
        return self.active

    def create(self, buy_price, sell_price, amount, trailing_stop):
        self.active = True
        self.initial_buy_price = buy_price
        self.initial_sell_price = sell_price

        self.max_buy_price = buy_price
        self.trailing_stop = trailing_stop

        self.amount = amount / buy_price

    def close(self, sell_price):
        self.active = False
        return self.amount * sell_price

    def check_trailing_stop(self, buy_point, sell_point):
        if self.max_buy_price < buy_point:
            self.max_buy_price = buy_point

        if self.max_buy_price - self.trailing_stop > buy_point:
            return self.close(sell_point)

        return 0

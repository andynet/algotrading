import functions
import api_functions
import time


class Order:
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


class Investigator:
    mode = 'negative'  # can be 'negative' (first = buying) or 'positive' (first = selling)  # TODO add neutral ???
    position = 0

    buying_prices = []
    selling_prices = []

    buying_points = []
    selling_points = []

    min_buying_price_value = None
    min_buying_price_position = None

    max_selling_price_value = None
    max_selling_price_position = None

    def examine(self, buying_price, selling_price):
        self.buying_prices.append(buying_price)
        self.selling_prices.append(selling_price)
        self.buying_points.append(0)
        self.selling_points.append(0)

        if self.min_buying_price_value is None or self.max_selling_price_value is None:
            self.min_buying_price_value = buying_price
            self.max_selling_price_value = selling_price

        if self.mode == 'negative' and self.min_buying_price_value > buying_price:
            self.min_buying_price_value = buying_price
            self.min_buying_price_position = self.position

        if self.mode == 'negative' and self.min_buying_price_value < selling_price:
            self.mode = 'positive'
            if self.max_selling_price_position is not None:
                self.selling_points[self.max_selling_price_position] = 1
                self.buying_points[self.min_buying_price_position] = 1
            self.max_selling_price_value = selling_price
            self.max_selling_price_position = self.position
            self.position += 1
            return self.buying_points, self.selling_points

        if self.mode == 'positive' and self.max_selling_price_value < selling_price:
            self.max_selling_price_value = selling_price
            self.max_selling_price_position = self.position

        if self.mode == 'positive' and self.max_selling_price_value > buying_price:
            self.mode = 'negative'
            if self.min_buying_price_position is not None:
                self.buying_points[self.min_buying_price_position] = 1
                self.selling_points[self.max_selling_price_position] = 1
            self.min_buying_price_value = buying_price
            self.min_buying_price_position = self.position
            self.position += 1
            return self.buying_points, self.selling_points

        self.position += 1
        return self.buying_points, self.selling_points

    # TODO implement
    def reset(self):
        pass


class Feeder:
    source = None
    position = 0

    buying_prices = []
    selling_prices = []

    def __init__(self, source):
        self.source = source
        if self.source != 'online':
            self.buying_prices, self.selling_prices = functions.read_input(self.source)

    def get_prices(self):
        if self.source == 'online':
            time.sleep(5)
            buying_price, selling_price = api_functions.get_price()
        else:
            if self.position >= len(self.buying_prices):
                buying_price, selling_price = None, None
            else:
                buying_price, selling_price = self.buying_prices[self.position], self.selling_prices[self.position]

        self.position += 1
        return buying_price, selling_price

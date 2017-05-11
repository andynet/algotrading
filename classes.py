import functions
import api_functions
import time


class Order:
    active = False
    initial_buy_price = 0
    initial_sell_price = 0

    max_buy_price = 0
    trailing_stop = 0

    units = 0

    def exists(self):
        return self.active

    def create(self, buy_price, sell_price, amount, trailing_stop):
        self.active = True
        self.initial_buy_price = buy_price
        self.initial_sell_price = sell_price

        self.max_buy_price = buy_price
        self.trailing_stop = trailing_stop

        self.units = amount / buy_price

    def close(self, sell_price):
        self.active = False
        return self.units * sell_price

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

    def get_results(self):
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


class FeaturesCreator:
    number = 7
    iterator = -1

    features = []
    buying_points_positions = []
    selling_points_positions = []

    def __init__(self, number):
        self.number = number

    def create_features(self, buying_prices, selling_prices, buying_points, selling_points):

        self.iterator += 1

        from_last_buy, from_last_sell = None, None
        last_optimal_buy, last_optimal_sell = None, None
        average_from_last_buy, average_from_last_sell = None, None
        average_buying_prices, average_selling_prices = None, None
        average_buying_duration, average_selling_duration = None, None

        buying_price = buying_prices[self.iterator]
        selling_price = selling_prices[self.iterator]

        if len(self.buying_points_positions) == 0:
            for i in range(0, self.iterator + 1):
                if buying_points[i] == 1:
                    self.buying_points_positions.append(i)
        else:
            for i in range(self.buying_points_positions[-1], self.iterator + 1):
                if buying_points[i] == 1:
                    self.buying_points_positions.append(i)

        if len(self.selling_points_positions) == 0:
            for i in range(0, self.iterator + 1):
                if selling_points[i] == 1:
                    self.selling_points_positions.append(i)
        else:
            for i in range(self.selling_points_positions[-1], self.iterator + 1):
                if selling_points[i] == 1:
                    self.selling_points_positions.append(i)

        if len(self.buying_points_positions) > 0:
            from_last_buy = self.iterator - self.buying_points_positions[-1]
            last_optimal_buy = buying_prices[self.buying_points_positions[-1]]
            average_from_last_buy = sum(buying_prices[self.buying_points_positions[-1]:(self.iterator + 1)]) / (
                from_last_buy + 1)

        if len(self.selling_points_positions) > 0:
            from_last_sell = self.iterator - self.selling_points_positions[-1]
            last_optimal_sell = selling_prices[self.selling_points_positions[-1]]
            average_from_last_sell = sum(selling_prices[self.selling_points_positions[-1]:(self.iterator + 1)]) / (
                from_last_sell + 1)

        if len(self.buying_points_positions) >= (self.number + 1):
            average_buying_prices = 0
            average_buying_duration = 0
            for j in range(self.number):
                average_buying_prices += buying_prices[self.buying_points_positions[-(1 + j)]]
                average_buying_duration += self.buying_points_positions[-(1 + j)] - self.buying_points_positions[
                    -(2 + j)]
            average_buying_prices /= self.number
            average_buying_duration /= self.number

        if len(self.selling_points_positions) >= (self.number + 1):
            average_selling_prices = 0
            average_selling_duration = 0
            for j in range(self.number):
                average_selling_prices += selling_prices[self.selling_points_positions[-(1 + j)]]
                average_selling_duration += self.selling_points_positions[-(1 + j)] - self.selling_points_positions[
                    -(2 + j)]
            average_selling_prices /= self.number
            average_selling_duration /= self.number

        result = [buying_price, selling_price,
                  from_last_buy, from_last_sell,
                  last_optimal_buy, last_optimal_sell,
                  average_from_last_buy, average_from_last_sell,
                  average_buying_prices, average_selling_prices,
                  average_buying_duration, average_selling_duration]

        self.features.append(result)

        return self.features


class LabelsCreator:
    iterator = 0
    labels = []

    def create_labels(self, buying_points, selling_points):

        for i in range(self.iterator + 1, len(buying_points)):
            if buying_points[i] == 1:
                new_labels = [4] * (i - (self.iterator + 1))
                new_labels.append(1)
                self.labels = self.labels[0:self.iterator + 1] + new_labels
                self.iterator = i
            if selling_points[i] == 1:
                new_labels = [2] * (i - (self.iterator + 1))
                new_labels.append(3)
                self.labels = self.labels[0:self.iterator + 1] + new_labels
                self.iterator = i
            if selling_points[i] == 0 and buying_points[i] == 0:
                self.labels.append(0)

        return self.labels

# coding=utf8
import csv


def get_triangles(symbol):
    reader = csv.reader(open('triangles.csv'))
    triangles = list()
    for row in reader:
        triangles.append(tuple(row))
    return filter(lambda t: symbol in t, triangles)


def get_trade_pairs():
    trade_pairs_side = dict()
    reader = csv.reader(open('trade_pairs.csv'))
    for row in reader:
        row = tuple(row)
        # let BTC->EOS be BUY for 'EOS/BTC'
        ticker = row[0]+row[1]
        trade_pairs_side[row] = ('SELL', ticker)
        trade_pairs_side[row[::-1]] = ('BUY', ticker)
    print(trade_pairs_side)
    return trade_pairs_side


class Triangle:
    def __init__(self):
        self.trade_pairs = get_trade_pairs()
        self.price_map = dict()
        self.max_diff = [0, None]
        self.trade_triangles = list()

    def _get_trade_triangle(self, symbol_a, symbol_b, symbol_c):
        return [self.trade_pairs[(symbol_a, symbol_b)],
                self.trade_pairs[(symbol_b, symbol_c)],
                self.trade_pairs[(symbol_c, symbol_a)]
                ]

    def prepare(self, symbol):
        # value: [(BUY/SELL, EOSBTC), (), ()]
        triangles = get_triangles(symbol)
        t_t = list()
        for t in triangles:
            t = list(t)
            t.remove(symbol)
            a, b = t[0], t[1]
            t_t.append(self._get_trade_triangle(symbol, a, b))
            t_t.append(self._get_trade_triangle(symbol, b, a))
        print(t_t)
        self.trade_triangles = t_t

    def update_price_map(self, ticker_price_list):
        for ticker_price in ticker_price_list:
            self.price_map[ticker_price['s']] = ticker_price

    def create_signal(self, ticker_price_list):
        self.update_price_map(ticker_price_list)
        self.calc()

    def calc(self):
        results = list()
        for triangle in self.trade_triangles:
            price1 = self._get_best_price(triangle[0][0], triangle[0][1])
            price2 = self._get_best_price(triangle[1][0], triangle[1][1])
            price3 = self._get_best_price(triangle[2][0], triangle[2][1])
            if price1 and price2 and price3:
                results.append(self._calc_diff([price1, price2, price3]))
        results = filter(lambda r: r[0] > 0, results)
        results.sort(key=lambda x: x[0], reverse=True)
        if len(results) > 0:
            self.max_diff = results[0] if self.max_diff[0] < results[0][0] else self.max_diff
        print('------statistics------')
        for result in results:
            print(result)
        print('------max_price------')
        print(self.max_diff)

    def _calc_diff(self, price_list):
        numerator = 1
        denominator = 1
        for price in price_list:
            if price[0] == 'BUY':
                denominator *= float(price[2])
            else:
                numerator *= float(price[2])
        return numerator / denominator - 1, price_list

    def _get_best_price(self, side, ticker):
        ticker_price = self.price_map.get(ticker)
        if ticker_price is None:
            return
        if side == 'BUY':
            price = ticker_price['a']
            quantity = ticker_price['A']
        else:
            price = ticker_price['b']
            quantity = ticker_price['B']
        return side, ticker, float(price), float(quantity), ticker_price['E']

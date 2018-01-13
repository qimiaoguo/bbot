import csv
from collections import defaultdict


def split_ticker_pair(ticker_pair):
    # ticker_pair = ticker_pair.encode('unicode-escape').decode('string_escape')
    src = dst = None
    if (ticker_pair[-3:] == 'BTC'):
        src = ticker_pair[:-3]
        dst = 'BTC'
    elif (ticker_pair[-3:] == 'ETH'):
        src = ticker_pair[:-3]
        dst = 'ETH'
    elif (ticker_pair[-3:] == 'BNB'):
        src = ticker_pair[:-3]
        dst = 'BNB'
    elif (ticker_pair[-4:] == 'USDT'):
        src = ticker_pair[:-4]
        dst = 'USDT'
    return src, dst


def parse(ticker_list):
    ticker_list = filter(lambda ticker: ticker['e'] == '24hrTicker', ticker_list)
    create_trade_pair(ticker_list)
    create_triangle()


trade_pairs = set()


def create_trade_pair(ticker_list):
    for ticker in ticker_list:
        trade_pairs.add(split_ticker_pair(ticker['s']))

    print(len(trade_pairs), trade_pairs)
    writer = csv.writer(open("trade_pairs.csv", 'wb'), dialect='excel')
    for row in sorted(trade_pairs):
        writer.writerow(row)


triangles = set()


def create_triangle():
    ticker_pair_map = defaultdict(set)
    for (src, dst) in trade_pairs:
        ticker_pair_map[src].add(dst)
        ticker_pair_map[dst].add(src)
    print(len(ticker_pair_map), ticker_pair_map)

    keys = sorted(ticker_pair_map.keys())
    for v1 in keys:
        for v2 in sorted(ticker_pair_map[v1]):
            if v2 <= v1:
                continue
            for v3 in sorted(ticker_pair_map[v2]):
                if v3 <= v2:
                    continue
                if v1 in ticker_pair_map[v3]:
                    triangles.add((v1, v2, v3))

    print(len(triangles), sorted(triangles))
    writer = csv.writer(open("triangles.csv", 'wb'), dialect='excel')
    for row in sorted(triangles):
        writer.writerow(sorted(row))

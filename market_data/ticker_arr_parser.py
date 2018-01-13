import csv
import json
from collections import defaultdict


def split_ticker_pair(ticker_pair):
    ticker_pair = ticker_pair.encode('unicode-escape').decode('string_escape')
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


ticker_pair_map = defaultdict(set)


def parse(ticker_list):
    ticker_list = filter(lambda ticker: ticker['e'] == '24hrTicker', ticker_list)
    ticker_pairs=[]
    for ticker in ticker_list:
        ticker_pairs.append(split_ticker_pair(ticker['s']))
    print(len(ticker_pairs), ticker_pairs)
    for (src, dst) in ticker_pairs:
        ticker_pair_map[src].add(dst)
        ticker_pair_map[dst].add(src)

    print(len(ticker_pair_map))
    #create btc triangle
    create_triangle()

graphs = set()


def create_triangle():
    keys = sorted(ticker_pair_map.keys())
    print keys
    for v1 in keys:
        for v2 in sorted(ticker_pair_map[v1]):
            if v2 <= v1:
                continue
            for v3 in sorted(ticker_pair_map[v2]):
                if v3 <= v2:
                    continue
                if v1 in ticker_pair_map[v3]:
                    graphs.add((v1, v2, v3))
    print(len(graphs), sorted(graphs))
    writer = csv.writer(open("triangles.csv", 'wb'), dialect='excel')
    for row in sorted(graphs):
        writer.writerow(sorted(row))

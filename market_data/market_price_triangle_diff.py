# coding=utf8
import csv
import json
import ssl

import websocket

from common import config
from signals.triangle_price_diff import Triangle

t = Triangle('BTC')


def on_message(ws, message):
    ticker_list = json.loads(message)
    t.create_signal(ticker_list)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("web socket closed")


def on_open(ws):
    print("web socket open")


def start_market_subscribe():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(config.bbot_config['wss_endpoint']+'/ws/!ticker@arr',
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


if __name__ == '__main__':
    start_market_subscribe()

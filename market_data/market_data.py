# coding=utf8
import json
import ssl

import websocket

import ticker_arr_parser
from common import config

try:
    import thread
except ImportError:
    import _thread as thread


def on_message(ws, message):
    ticker_arr_parser.parse(json.loads(message))


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("web socket closed")


def on_open(ws):
    print("web socket open")


def generate_url(subscriptions):
    pass


def start_market_subscribe():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(config.bbot_config['wss_endpoint']+'/ws/!ticker@arr',
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

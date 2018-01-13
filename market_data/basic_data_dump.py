# coding=utf8
import json
import ssl
import threading
from time import sleep

import websocket

import ticker_arr_parser
from common import config


def on_message(ws, message):
    ticker_arr_parser.parse(json.loads(message))


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("web socket closed")


def on_open(ws):
    print("web socket open")


def basic_data_dump():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(config.bbot_config['wss_endpoint']+'/ws/!ticker@arr',
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)
    t = threading.Thread(target=stop_ws, args=(ws,))
    t.start()
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


def stop_ws(ws):
    print('will stop after 45 seconds')
    sleep(45)
    ws.close()
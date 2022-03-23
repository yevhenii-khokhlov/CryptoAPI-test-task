import json
import requests
import websocket
from django.core.cache import cache


def get_binance_pairs():
    response = requests.get('https://api.binance.com/api/v1/exchangeInfo')
    data = json.loads(response.text)
    pairs = [f'{item["baseAsset"]}{item["quoteAsset"]}' for item in data['symbols']]

    cache.set('binance_pairs', pairs)

    return pairs


BINANCE_PAIRS = get_binance_pairs()


# Define WebSocket callback functions
def ws_message(ws, message_text):
    message = json.loads(message_text)
    key = f'B_{message["s"]}'
    cache.set(key, message)
    print(f'BINANCE {message}')


def ws_close(ws):
    print('Connection closed')


def ws_error(ws):
    print("BINANCE ERROR")


def binance_ws_thread(*args):
    url = f'wss://stream.binance.com:9443/ws/!bookTicker'
    ws = websocket.WebSocketApp(
        url,
        on_message=ws_message,
        on_close=ws_close,
        on_error=ws_error
    )
    ws.run_forever()

import json
import requests
import websocket
from django.core.cache import cache


def get_kraken_pairs():
    response = requests.get('https://api.kraken.com/0/public/AssetPairs')
    data = json.loads(response.text)['result']

    pairs = []
    for key in data.keys():
        pairs.append(data[key]['wsname'].replace('\\', ''))

    cache.set('kraken_pairs', pairs)

    return pairs


# Define WebSocket callback functions
def ws_message(ws, message_text):
    message = json.loads(message_text)
    key = f'K_{message[-1]}'
    print(f'KRAKEN {message}')
    cache.set(key, message)


def ws_open(ws):
    kraken_pairs = get_kraken_pairs()
    ws.send('{"event":"subscribe", "subscription":{"name":"ticker"}, "pair":%s}' % str(kraken_pairs).replace("'", '"'))


def kraken_ws_thread(*args):
    ws = websocket.WebSocketApp("wss://ws.kraken.com/", on_open=ws_open, on_message=ws_message)
    ws.run_forever()

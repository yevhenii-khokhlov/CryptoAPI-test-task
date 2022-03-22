import websocket

from django.core.cache import cache


def on_massage_binance(ws, message):
    cache.set('binance_pairs', message, 61)
    print(f'binance upd {len(message)} items')


def on_close_binance(ws):
    print('Connection closed')


def start_binance():
    ws = websocket.WebSocketApp(
        'wss://stream.binance.com:9443/ws/!miniTicker@arr',
        on_message=on_massage_binance,
        on_close=on_close_binance
    )
    ws.run_forever()

import websocket

from CryptoAPI.settings import binance_pairs


def on_massage_binance(ws, message):
    print('binance upd')
    binance_pairs.update({"pairs": message})


def on_close_binance(ws):
    print('Connection closed')


def start_binance():
    ws = websocket.WebSocketApp(
        'wss://stream.binance.com:9443/ws/!miniTicker@arr',
        on_message=on_massage_binance,
        on_close=on_close_binance
    )
    ws.run_forever()

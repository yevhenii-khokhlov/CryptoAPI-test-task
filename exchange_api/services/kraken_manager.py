from kraken_wsclient_py import kraken_wsclient_py as client


def start_kraken():
    pass


def my_handler(message):
    # Here you can do stuff with the messages
    print(message)

my_client = client.WssClient()
my_client.start()

# Sample public-data subscription:

my_client.subscribe_public(
    subscription = {
        'name': 'trade'
    },
    pair = ['XBT/USD', 'XRP/USD'],
    callback = my_handler
)
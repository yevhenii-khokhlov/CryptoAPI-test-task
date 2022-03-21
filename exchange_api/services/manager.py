from CryptoAPI.settings import binance_pairs, kraken_pairs
from exchange_api.errors import UnknownProcessingError


def get_prices_on_exchange(pair, exchange) -> list:
    try:
        if not exchange and not pair:
            return get_all_pairs_from_all_exchanges()

        if exchange and not pair:
            return get_all_pairs_from(exchange)

        if exchange and pair:
            return get_pair_from(pair, exchange)

        return []

    except Exception as err:
        raise UnknownProcessingError(err.__str__())


def get_all_pairs_from_all_exchanges():
    return [{"SDR/AWD": {}}, {"AWD/AAS": {}}]


def get_all_pairs_from(exchange):
    if exchange == 'binance':
        print(binance_pairs)
        return binance_pairs['pairs']

    if exchange == 'kraken':
        return kraken_pairs

    raise Exception(f'Wrong exchange {exchange}')


def get_pair_from(pair, exchange):
    if exchange == 'binance':
        price = get_pare_price_from_binance(pair)
        return [price]

    if exchange == 'kraken':
        price = get_pare_price_from_kraken(pair)
        return [price]

    raise Exception(f'Wrong exchange {exchange}')


def get_pare_price_from_binance(pair):
    for item in binance_pairs:
        if item['s'] == pair.replace('/', ''):
            return [item]

    raise Exception(f'Pair not found {pair}')


def get_pare_price_from_kraken(pair):
    return [{"SDR/AWD": {}}]

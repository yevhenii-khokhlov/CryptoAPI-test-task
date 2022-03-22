import json

from django.core.cache import cache

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
        pairs = json.loads(cache.get('binance_pairs'))
        parsed_pares = [parse_binance_pair(p) for p in pairs]

        return parsed_pares

    if exchange == 'kraken':
        pairs = json.loads(cache.get('kraken_pairs'))
        return pairs

    raise Exception(f'Wrong exchange {exchange}')


def get_pair_from(pair, exchange):
    if exchange == 'binance':
        price = get_pare_price_from_binance(pair)
        return [price]

    if exchange == 'kraken':
        price = get_pare_price_from_kraken(pair)
        return [price]

    raise Exception(f'Wrong exchange {exchange}')


def get_pare_price_from_binance(pair_name):
    binance_pairs = json.loads(cache.get('binance_pairs'))
    parsed_pair = pair_name.replace('/', '')

    for item in binance_pairs:
        if item['s'] == parsed_pair:
            pair = parse_binance_pair(item, pair_name)
            return [pair]

    raise Exception(f'Pair not found {parsed_pair}')


def get_pare_price_from_kraken(pair):
    return [{"SDR/AWD": {}}]


def parse_binance_pair(pair, name=None):
    return {
        'pair': name if name else pair['s'],
        'close_price': pair['c'],
        'open_price': pair['o'],
        'high_price': pair['h'],
        'low_price': pair['l']
    }


def parse_kraken_pair(pair, name=None):
    return {
        'pair': name if name else pair['s'],
        'close_price': pair['c'],
        'open_price': pair['o'],
        'high_price': pair['h'],
        'low_price': pair['l']
    }

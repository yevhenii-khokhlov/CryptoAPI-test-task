from django.core.cache import cache

from exchange_api.errors import UnknownProcessingError


def get_prices_on_exchange(pair, exchange):
    try:
        if not exchange and not pair:
            return get_all_pairs_from_all_exchanges()

        if exchange and not pair:
            return get_all_pairs_from(exchange)

        if exchange and pair:
            return get_pair_from(pair, exchange)

        return {}

    except Exception as err:
        raise UnknownProcessingError(err.__str__())


def get_all_pairs_from_all_exchanges():
    binance_prices = get_all_pairs_prices_from_binance()
    kraken_prices = get_all_pairs_prices_from_kraken()
    average_prices = {}

    binance_pairs = binance_prices.keys()
    for binance_pair in binance_pairs:
        kraken_price = kraken_prices.get(binance_pair)
        binance_price = binance_prices.get(binance_pair)

        if binance_price and kraken_price:
            average_price = round((binance_price + kraken_price) / 2, 6)
            average_prices.update({binance_pair: average_price})

        elif binance_price and not kraken_price:
            average_prices.update({binance_pair: binance_price})

    return average_prices


def get_all_pairs_from(exchange):
    if exchange == 'binance':
        return get_all_pairs_prices_from_binance()

    if exchange == 'kraken':
        return get_all_pairs_prices_from_kraken()


def get_all_pairs_prices_from_binance():
    pairs = cache.get('binance_pairs')
    print(f'Pairs {pairs}')
    prices = {}

    for pair in pairs:
        price = get_pare_price_from_binance(pair)
        prices.update({pair: price})

    return prices


def get_all_pairs_prices_from_kraken():
    pairs = cache.get('kraken_pairs')
    prices = {}

    for pair in pairs:
        price = get_pare_price_from_kraken(pair)
        prices.update({pair: price})

    return prices


def get_pair_from(pair, exchange):
    if exchange == 'binance':
        price = get_pare_price_from_binance(pair)
        return {pair: price}

    if exchange == 'kraken':
        price = get_pare_price_from_kraken(pair)
        return {pair: price}


def get_pare_price_from_binance(pair):
    pair_info = cache.get(f'B_{pair.replace("/", "")}')
    if pair_info:
        price = (float(pair_info['a']) + float(pair_info['b'])) / 2
        return round(price, 6)

    return 0.0


def get_pare_price_from_kraken(pair):
    pair_info = cache.get(f'K_{pair}')
    if pair_info:
        price = (float(pair_info[1]['a'][0]) + float(pair_info[1]['b'][0])) / 2
        return round(price, 6)

    return 0.0

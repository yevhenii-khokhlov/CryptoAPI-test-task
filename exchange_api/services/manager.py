from django.core.cache import cache

from exchange_api.errors import UnknownProcessingError


def get_prices_on_exchange(pair, exchange):
    pair = pair.replace('/', '') if pair else None
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
    average_prices = {}

    all_pairs = cache.get('binance_pairs')
    all_pairs.extend(cache.get('kraken_pairs'))
    unique_pairs = set(all_pairs)

    for pair in unique_pairs:
        b_price = get_pare_price_from_binance(pair)
        k_price = get_pare_price_from_kraken(pair)

        if not b_price and k_price:
            average_prices.update({pair: k_price})

        if not k_price and b_price:
            average_prices.update({pair: b_price})

        if b_price and k_price:
            average = (b_price + k_price) / 2
            average_prices.update({pair: average})

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
    pair_info = cache.get(f'B_{pair}')
    if pair_info:
        price = (float(pair_info['a']) + float(pair_info['b'])) / 2
        return price

    return


def get_pare_price_from_kraken(pair):
    pair_info = cache.get(f'K_{pair}')
    if pair_info:
        price = (float(pair_info[1]['a'][0]) + float(pair_info[1]['b'][0])) / 2
        return price

    return

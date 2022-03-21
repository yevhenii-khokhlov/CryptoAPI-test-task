from __future__ import absolute_import, unicode_literals

from celery import shared_task

from exchange_api.services.binanse_manager import start_binance
from exchange_api.services.kraken_manager import start_kraken


@shared_task
def background_start_binance():
    print('Start binance')
    start_binance()


@shared_task
def background_start_kraken():
    print('Start kraken')
    start_kraken()


background_start_binance.delay()
background_start_kraken.delay()


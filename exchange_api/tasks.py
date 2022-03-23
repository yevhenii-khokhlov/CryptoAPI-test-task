from __future__ import absolute_import, unicode_literals

import _thread

from exchange_api.services.kraken_manager import kraken_ws_thread
from exchange_api.services.binance_manager import binance_ws_thread


_thread.start_new_thread(kraken_ws_thread, ())
_thread.start_new_thread(binance_ws_thread, ())

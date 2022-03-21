import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from exchange_api.errors import UnknownProcessingError
from exchange_api.services.manager import get_prices_on_exchange


@require_http_methods(["GET", ])
def prices_on_exchanges(request):
    """
    GET - pair as 'BTK/EUR' string ('/' as delimiter)
        - exchange as lowercase string;

    :param request: {
        pair: str, None,
        exchange: str, None
    }
    :return: {
        success: bool,
        exchange: list
    }
    """
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        couple = body.get('pair')
        exchange = body.get('exchange')

        prices_on_exchange = get_prices_on_exchange(
            pair=couple,
            exchange=exchange
        )
        return JsonResponse({"success": True, "exchange": prices_on_exchange})

    except UnknownProcessingError as err:
        return JsonResponse({"success": False, "error": err.__str__()})

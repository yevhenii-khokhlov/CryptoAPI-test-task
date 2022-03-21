from django.urls import path

from .views import prices_on_exchanges


urlpatterns = [
    path('', prices_on_exchanges),
]

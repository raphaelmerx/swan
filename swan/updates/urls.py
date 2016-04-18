from django.conf.urls import url
from django.conf import settings

from .views import telegram_webhook


urlpatterns = [
    url(settings.TELEGRAM_TOKEN, telegram_webhook, name='telegram_webhook'),
]

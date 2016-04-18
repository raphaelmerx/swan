from rest_framework.decorators import api_view
from django.http import HttpResponse


@api_view(http_method_names=['POST'])
def telegram_webhook(request):
    print(request)
    return HttpResponse('')

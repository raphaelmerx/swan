from rest_framework.decorators import api_view
from django.http import HttpResponse

from .models import Chat


@api_view(http_method_names=['POST'])
def telegram_webhook(request):
    # {'update_id': 104740320, 'message': {'date': 1461021341, 'chat': {'first_name': 'Raphael', 'id': 173413525, 'type': 'private', 'last_name': 'Merx'}, 'text': 'hihi', 'from': {'first_name': 'Raphael', 'id': 173413525, 'last_name': 'Merx'}, 'message_id': 14}}
    update = request.data
    chat_id = update['message']['chat']['id']
    chat = Chat.objects.get_or_create(chat_id=chat_id)
    print(chat)
    print(request.data)
    return HttpResponse('')

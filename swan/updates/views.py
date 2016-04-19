from rest_framework.decorators import api_view
from django.http import HttpResponse

from .models import Chat


@api_view(http_method_names=['POST'])
def telegram_webhook(request):
    update = request.data
    chat_id = update['message']['chat']['id']
    chat, _ = Chat.objects.get_or_create(chat_id=chat_id)
    if 'text' in update['message']:
        message_text = update['message']['text']
        if message_text.startswith('/token '):
            token = message_text.strip('/token ')
            chat.api_token = token
            chat.save()
        elif message_text.startswith('/batch '):
            batch_id = message_text.strip('/batch ')
            # TODO: error message if batch id is not an integer
            chat.batch_id = int(batch_id)
            chat.save()
    elif 'photo' in update['message']:
        # upload the file to Shreddr
        file_contents = Chat.get_file_contents(update)
        chat.upload_file(file_contents, file_name=str(update['message']['date']))
        # TODO: send a message to the user about file upload
    return HttpResponse()

from datetime import datetime

import pytz
from rest_framework.decorators import api_view
from django.http import HttpResponse

from .models import Chat


def get_date_isoformat_from_epoch(epoch):
    return datetime.fromtimestamp(epoch, pytz.utc).strftime('%Y-%m-%d %H:%M:%S %Z')


@api_view(http_method_names=['POST'])
def telegram_webhook(request):
    update = request.data
    chat_id = update['message']['chat']['id']
    chat, _ = Chat.objects.get_or_create(chat_id=chat_id)

    if 'text' in update['message']:
        message_text = update['message']['text']
        if message_text == '/start':
            chat.send_message('hey stranger')
        elif message_text.startswith('/token '):
            token = message_text.strip('/token ')
            chat.api_token = token
            chat.save()
            chat.send_message('Token saved.')
        elif message_text.startswith('/new '):
            batch_name = message_text.strip('/new ')
            batch_id = chat.create_batch(batch_name)
            chat.send_message('Sucess! Batch {} created.\n'
                              'Send "/batch {}" to start uploading files to this batch.'.format(batch_id, batch_id))
        elif message_text.startswith('/batch '):
            batch_id = message_text.strip('/batch ')
            # TODO: error message if batch id is not an integer
            chat.batch_id = int(batch_id)
            chat.save()
            chat.send_message('Batch ID saved.')
        elif message_text.startswith('/submit'):
            success, error = chat.submit_batch()
            if success:
                chat.send_message('Batch successfully submitted.')
            else:
                chat.send_message('Error: {}'.format(error))
        elif message_text.startswith('/documents'):
            chat.send_message(chat.list_documents())
        elif message_text.startswith('/batches'):
            chat.send_message(chat.list_batches())
        elif message_text.startswith('/associate_document '):
            document_id = message_text.strip('/associate_document ')
            success = chat.associate_document(document_id)
            if success:
                chat.send_message('Successfully associated document {} with batch {}'.format(
                    chat.document_id, chat.batch_id))
            else:
                chat.send_message('Error associating document {} with batch {}'.format(
                    document_id, chat.batch_id))
        else:
            chat.send_message('Unrecognized command. Say what?')
    elif 'photo' in update['message']:
        if not chat.batch_id or not chat.api_token:
            chat.send_message('Please provide a token and a batch ID before sending form images.')
        else:
            # upload the file to Shreddr
            file_contents = Chat.get_file_contents(update)
            file_name = get_date_isoformat_from_epoch(update['message']['date'])
            chat.upload_file(file_contents, file_name=file_name)
            chat.send_message('File successfully uploaded with name "{}".'.format(file_name))
    return HttpResponse()

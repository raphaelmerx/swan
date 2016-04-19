import json
import requests

from django.db import models
from django.conf import settings


class Chat(models.Model):
    chat_id = models.IntegerField()
    api_token = models.CharField(max_length=100, null=True)
    batch_id = models.IntegerField(null=True)

    @staticmethod
    def get_file_contents(update):
        images = update['message']['photo']
        file_id = max(images, key=lambda image: image['height'])['file_id']
        getFile_response = requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(
            settings.TELEGRAM_TOKEN, file_id))
        getFile_response = json.loads(getFile_response.content.decode())
        assert getFile_response['ok']
        file_path = getFile_response['result']['file_path']
        # download file contents using the file/bot API
        response = requests.get('https://api.telegram.org/file/bot{}/{}'.format(settings.TELEGRAM_TOKEN, file_path))
        return response.content

    def upload_file(self, file_contents, file_name):
        batch_files_endpoint = 'https://shreddr.captricity.com/api/v1/batch/{}/batch-file/'.format(self.batch_id)
        session = requests.Session()
        session.headers.update({'Captricity-API-Token': '{}'.format(self.api_token)})
        files = {'uploaded_file': file_contents}
        response = session.post(batch_files_endpoint, data={'file_name': file_name}, files=files)
        return True

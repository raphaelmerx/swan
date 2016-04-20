import json
import requests

from django.db import models
from django.conf import settings
from django.utils.functional import cached_property


class Chat(models.Model):
    chat_id = models.IntegerField()
    api_token = models.CharField(max_length=100, null=True)
    batch_id = models.IntegerField(null=True)

    def __repr__(self):
        return str(self.__dict__)

    @cached_property
    def shreddr_session(self):
        session = requests.Session()
        session.headers.update({'Captricity-API-Token': '{}'.format(self.api_token)})
        return session

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
        files = {'uploaded_file': file_contents}
        self.shreddr_session.post(batch_files_endpoint, data={'file_name': file_name}, files=files)
        return True

    def send_message(self, text):
        response = requests.post('https://api.telegram.org/bot{}/sendMessage'.format(settings.TELEGRAM_TOKEN),
                                 data={'chat_id': self.chat_id, 'text': text})
        assert response.status_code == 200

    def submit_batch(self):
        batch_endpoint = 'https://shreddr.captricity.com/api/v1/batch/{}/submit'.format(self.batch_id)
        response = self.shreddr_session.post(batch_endpoint)
        if response.status_code == 200:
            return (True, '')
        else:
            error = json.loads(response.content.decode())['readiness']['errors'][0]
            return (False, error)

    def create_batch(self, name):
        batch_endpoint = 'https://shreddr.captricity.com/api/v1/batch'
        response = self.shreddr_session.post(batch_endpoint, data={'name': name})
        return response

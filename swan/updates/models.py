from django.db import models


class Chat(models.Model):
    chat_id = models.IntegerField()
    api_token = models.CharField(max_length=100, null=True)
    batch_id = models.IntegerField(null=True)

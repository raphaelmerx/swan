# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-20 19:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0002_auto_20160418_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='document_id',
            field=models.IntegerField(null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-16 13:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_user_listroot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='listroot',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 02:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0009_auto_20171122_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='text',
            field=models.TextField(default=''),
        ),
    ]

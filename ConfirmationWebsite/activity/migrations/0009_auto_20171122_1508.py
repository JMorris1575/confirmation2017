# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-22 20:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0008_auto_20171117_2229'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Page',
            new_name='Action',
        ),
        migrations.AddField(
            model_name='activity',
            name='overview',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]

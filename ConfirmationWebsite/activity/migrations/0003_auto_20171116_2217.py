# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-17 03:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_auto_20171116_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='number',
            field=models.IntegerField(),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-25 02:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0012_auto_20171124_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userresponse',
            name='action',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='activity.Action'),
            preserve_default=False,
        ),
    ]

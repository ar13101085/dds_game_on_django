# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-09 08:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_scrap', '0002_auto_20170909_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]

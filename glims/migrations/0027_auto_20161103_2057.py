# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-03 20:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0026_auto_20161101_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pool',
            name='name',
            field=models.CharField(db_index=True, max_length=100, unique=True),
        ),
    ]

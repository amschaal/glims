# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-07 00:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0008_auto_20160503_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='lab',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]

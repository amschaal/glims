# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-19 23:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0021_auto_20161019_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='library',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]

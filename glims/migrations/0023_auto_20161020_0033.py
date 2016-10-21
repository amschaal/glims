# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-20 00:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0022_library_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pool',
            old_name='sample_data',
            new_name='library_data',
        ),
        migrations.AlterField(
            model_name='library',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-25 18:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0003_remove_lab_cloudstore'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='lab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='glims.Lab'),
        ),
    ]

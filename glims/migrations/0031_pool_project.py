# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-10-23 21:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0030_auto_20171020_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='pool',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='glims.Project'),
        ),
    ]
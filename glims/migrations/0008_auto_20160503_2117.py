# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-03 21:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0007_project_related_projects'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modeltypeplugins',
            name='plugin',
        ),
        migrations.RemoveField(
            model_name='modeltypeplugins',
            name='type',
        ),
        migrations.RemoveField(
            model_name='plugin',
            name='model_types',
        ),
        migrations.DeleteModel(
            name='ModelTypePlugins',
        ),
        migrations.DeleteModel(
            name='Plugin',
        ),
    ]
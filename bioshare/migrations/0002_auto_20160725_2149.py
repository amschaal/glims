# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 21:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bioshare', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='projectshare',
            unique_together=set([('project', 'labshare'), ('labshare', 'folder')]),
        ),
    ]
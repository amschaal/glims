# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bioinformatics', '0003_auto_20160112_1822'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bioinfoproject',
            name='assigned_to',
        ),
        migrations.AddField(
            model_name='bioinfoproject',
            name='manager',
            field=models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='bioinfoproject',
            name='participants',
            field=models.ManyToManyField(related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]

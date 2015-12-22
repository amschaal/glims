# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0005_auto_20151222_1958'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BioinfoProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('assigned_to', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('project', models.OneToOneField(to='glims.Project')),
            ],
        ),
    ]

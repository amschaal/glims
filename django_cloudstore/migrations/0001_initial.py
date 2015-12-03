# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CloudStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('storage_engine', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('attributes', jsonfield.fields.JSONField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

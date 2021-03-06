# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-20 21:20
from __future__ import unicode_literals

import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('extensible', '0001_initial'),
        ('glims', '0024_library_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', django.contrib.postgres.fields.hstore.HStoreField(blank=True, default=dict, null=True)),
                ('name', models.CharField(max_length=100)),
                ('barcode', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='extensible.ModelType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='barcode',
            name='type',
        ),
        migrations.RemoveField(
            model_name='library',
            name='barcode',
        ),
        migrations.DeleteModel(
            name='Barcode',
        ),
        migrations.AddField(
            model_name='library',
            name='adapter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='libraries', to='glims.Adapter'),
        ),
    ]

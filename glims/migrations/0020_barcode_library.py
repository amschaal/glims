# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-19 23:16
from __future__ import unicode_literals

import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('extensible', '0001_initial'),
        ('glims', '0019_project_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Barcode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', django.contrib.postgres.fields.hstore.HStoreField(blank=True, default=dict, null=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='extensible.ModelType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', django.contrib.postgres.fields.hstore.HStoreField(blank=True, default=dict, null=True)),
                ('name', models.CharField(max_length=100)),
                ('barcode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='glims.Barcode')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='glims.Sample')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='extensible.ModelType')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

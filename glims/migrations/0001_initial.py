# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django.db.models.deletion
import glims.lims


class Migration(migrations.Migration):

    dependencies = [
        ('extensible', '0001_initial'),
        ('django_cloudstore', '0002_cloudstore_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('subject', models.CharField(max_length=250)),
                ('body', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailRecipient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=75)),
                ('sent', models.DateTimeField(null=True, blank=True)),
                ('email', models.ForeignKey(related_name='recipients', to='glims.Email')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=250)),
                ('body', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('slug', models.SlugField(max_length=20, unique=True, null=True)),
                ('cloudstore', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='django_cloudstore.CloudStore', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ModelTypePlugins',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.IntegerField(default=0)),
                ('layout', models.CharField(max_length=10, choices=[(b'inline', b'Inline'), (b'tabbed', b'Tab')])),
                ('header', models.CharField(max_length=30, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Plugin',
            fields=[
                ('id', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('app', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('page', models.CharField(max_length=50)),
                ('template', models.CharField(max_length=250)),
                ('model_types', models.ManyToManyField(related_name='plugins', null=True, through='glims.ModelTypePlugins', to='extensible.ModelType', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('created', models.DateField(auto_now=True)),
                ('sample_data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
                ('project_id', models.CharField(default=glims.lims.generate_project_id, max_length=4, unique=True, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('lab', models.ForeignKey(to='glims.Lab')),
                ('sample_type', models.ForeignKey(related_name='+', blank=True, to='extensible.ModelType', null=True)),
                ('type', models.ForeignKey(blank=True, to='extensible.ModelType', null=True)),
            ],
            options={
                'permissions': (('view', 'View Project'), ('admin', 'Administer Project'), ('pi', 'Can PI a Project')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
                ('sample_id', models.CharField(unique=True, max_length=60)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('received', models.DateField(null=True, blank=True)),
                ('project', models.ForeignKey(related_name='samples', blank=True, to='glims.Project', null=True)),
                ('type', models.ForeignKey(blank=True, to='extensible.ModelType', null=True)),
            ],
            options={
                'permissions': (('view', 'View Sample'), ('admin', 'Administer Sample')),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pool',
            name='samples',
            field=models.ManyToManyField(related_name='pools', to='glims.Sample'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pool',
            name='type',
            field=models.ForeignKey(blank=True, to='extensible.ModelType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='modeltypeplugins',
            name='plugin',
            field=models.ForeignKey(to='glims.Plugin'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='modeltypeplugins',
            name='type',
            field=models.ForeignKey(to='extensible.ModelType'),
            preserve_default=True,
        ),
    ]

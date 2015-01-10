# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_hstore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('glims', '0005_modeltype_schema'),
    ]

    operations = [
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', django_hstore.fields.DictionaryField()),
                ('refs', django_hstore.fields.ReferencesField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProcessTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('type', models.ForeignKey(to='glims.ModelType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', django_hstore.fields.DictionaryField()),
                ('refs', django_hstore.fields.ReferencesField()),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('type', models.ForeignKey(blank=True, to='glims.ModelType', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkflowProcess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField()),
                ('process', models.ForeignKey(to='glims.ProcessTemplate')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkflowTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('process_templates', models.ManyToManyField(to='glims.ProcessTemplate', through='glims.WorkflowProcess')),
                ('type', models.ForeignKey(to='glims.ModelType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='workflowprocess',
            name='workflow',
            field=models.ForeignKey(to='glims.WorkflowTemplate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workflow',
            name='workflow_template',
            field=models.ForeignKey(to='glims.WorkflowTemplate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='process',
            name='process_template',
            field=models.ForeignKey(to='glims.ProcessTemplate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='process',
            name='type',
            field=models.ForeignKey(blank=True, to='glims.ModelType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='process',
            name='workflow',
            field=models.ForeignKey(to='glims.Workflow'),
            preserve_default=True,
        ),
    ]

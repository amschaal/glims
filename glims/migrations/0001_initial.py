# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('status', models.CharField(max_length=50, null=True, blank=True)),
                ('path', models.CharField(max_length=250)),
                ('job_id', models.CharField(max_length=75, null=True, blank=True)),
                ('args', jsonfield.fields.JSONField(default=[], null=True, blank=True)),
                ('config', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
                ('data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JobSubmission',
            fields=[
                ('id', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('job_name', models.CharField(max_length=100, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('submitter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ModelType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_type', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('schema', jsonfield.fields.JSONField(null=True, blank=True)),
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
            name='Process',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
                ('sample_data', jsonfield.fields.JSONField(null=True, blank=True)),
                ('type', models.ForeignKey(blank=True, to='glims.ModelType', null=True)),
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
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('group', models.ForeignKey(to='auth.Group')),
                ('type', models.ForeignKey(blank=True, to='glims.ModelType', null=True)),
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
                ('type', models.ForeignKey(blank=True, to='glims.ModelType', null=True)),
            ],
            options={
                'permissions': (('view', 'View Sample'), ('admin', 'Administer Sample')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', jsonfield.fields.JSONField(default={}, null=True, blank=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('created', models.DateField(auto_now=True)),
                ('pool', models.ForeignKey(blank=True, to='glims.Pool', null=True)),
                ('samples', models.ManyToManyField(to='glims.Sample')),
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
                ('process', models.ForeignKey(related_name='+', to='glims.ModelType')),
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
                ('processes', models.ManyToManyField(related_name='+', through='glims.WorkflowProcess', to='glims.ModelType')),
                ('type', models.ForeignKey(related_name='+', to='glims.ModelType')),
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
            name='workflow',
            field=models.ForeignKey(related_name='processes', to='glims.Workflow'),
            preserve_default=True,
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
            field=models.ForeignKey(blank=True, to='glims.ModelType', null=True),
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
            field=models.ForeignKey(to='glims.ModelType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='modeltype',
            name='plugins',
            field=models.ManyToManyField(to='glims.Plugin', null=True, through='glims.ModelTypePlugins', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='submission',
            field=models.ForeignKey(related_name='jobs', blank=True, to='glims.JobSubmission', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ClusterJob',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('glims.job',),
        ),
        migrations.CreateModel(
            name='DRMAAJob',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('glims.job',),
        ),
        migrations.CreateModel(
            name='SGE',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('glims.drmaajob',),
        ),
    ]

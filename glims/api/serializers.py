from rest_framework import serializers
from glims.lims import Project, Sample, ModelType, Pool, Lab
from django_compute.models import Job

# from jsonfield import JSONField
from glims.models import StatusOption
from django.contrib.auth.models import User
from rest_framework.fields import DictField
from extensible.drf import DRFFieldHandler
from glims.api.fields import JSONField, ModelRelatedField

class ModelTypeSerializer(serializers.ModelSerializer):
    content_type__model = serializers.CharField(source='content_type.model')
    fields = JSONField()
    class Meta:
        model = ModelType
        field=('name','description','fields','content_type__model')

class DataSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields',None)
        if fields:
            serializer_fields = DRFFieldHandler(fields).get_fields()
            for key,field in serializer_fields.items():
                self.fields[key] = field
        super(DataSerializer, self).__init__(*args,**kwargs)

class ExtensibleSerializer(serializers.ModelSerializer):
    type = ModelRelatedField(model=ModelType,serializer=ModelTypeSerializer)
    type__name = serializers.StringRelatedField(source='type.name',read_only=True)
    data = DictField()
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields',None)
        super(ExtensibleSerializer, self).__init__(*args,**kwargs)
        if fields:
            self.fields['data'] = DataSerializer(fields=fields)
    def update(self, instance, validated_data):
        self.fields['data'] = DictField() #hacky, figure out how to serialize to nested DataSerializer
        validated_data['data'] = {key:str(value) for key,value in validated_data.get('data',{}).items()} #HStore only takes strings
        return super(ExtensibleSerializer, self).update(instance,validated_data)
    def create(self, validated_data):
        self.fields['data'] = DictField() #hacky, figure out how to serialize to nested DataSerializer
        validated_data['data'] = {key:str(value) for key,value in validated_data.get('data',{}).items()} #HStore only takes strings
        return super(ExtensibleSerializer, self).create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','last_login','first_name','last_name','email','groups')

class StatusOptionSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="status.id")
    name = serializers.CharField(source="status.name")
    class Meta:
        model = StatusOption
        fields = ('id','name','order')
         
class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab

class ProjectSerializer(ExtensibleSerializer):
    lab__name = serializers.CharField(source='lab.name',read_only=True)
    sample_type = ModelRelatedField(model=ModelType,serializer=ModelTypeSerializer)
    type__name = serializers.StringRelatedField(source='type.name',read_only=True)
    status_options = StatusOptionSerializer(many=True,read_only=True,source='type.status_options')
    lab = ModelRelatedField(model=Lab,serializer=LabSerializer)
    history = JSONField(read_only=True)
    class Meta:
        model = Project
#         fields = ('id','name','type','type__name','sample_type','description','lab','lab__name','data','created','status','history','status_options')

        
class SampleSerializer(ExtensibleSerializer):
    project__name = serializers.CharField(source='project.name',read_only=True)
    class Meta:
        model = Sample
        read_only_fields = ('sample_id','project__name','type__name')
#         fields = ('id','sample_id','project_id','name','description','project'lab','lab__name','data')
#         fields = ('id','sample_id','project_id','name','description','project__name')

class PoolSerializer(ExtensibleSerializer):
    type__name = serializers.StringRelatedField(source='type.name')
    sample_data = JSONField()
    class Meta:
        model = Pool

class JobSerializer(serializers.ModelSerializer):
    data = JSONField()
    params = JSONField()
    args = JSONField()
    class Meta:
        model = Job
        fields = ('id','job_id','template','params','created','run_at','args','status','data')



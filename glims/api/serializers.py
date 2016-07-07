from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.fields import DictField

from django_compute.models import Job
from extensible.drf.serializers import ExtensibleSerializer, ModelTypeSerializer,\
    FlatModelTypeSerializer
from glims.api.fields import JSONField, ModelRelatedField
from glims.lims import Project, Sample, ModelType, Pool, Lab
from glims.models import Status


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    def get_name(self, user):
        return '%s %s'%(user.first_name,user.last_name)
        
    class Meta:
        model = User
        fields = ('id','name','last_login','first_name','last_name','email','groups')

class FlatUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    def get_name(self, user):
        return '%s %s'%(user.first_name,user.last_name)
    class Meta:
        model = User
        fields = ('id','name','first_name','last_name','email')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id','name')


class StatusSerializer(serializers.ModelSerializer):
#     id = serializers.CharField(source="status.id")
#     name = serializers.CharField(source="status.name")
    class Meta:
        model = Status
#         fields = ('id','name','order')
         
class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab

class BasicProjectSerializer(serializers.ModelSerializer):
    lab__name = serializers.CharField(source='lab.name',read_only=True)
    group__name = serializers.CharField(source='group.name',read_only=True)
    class Meta:
        model = Project
        fields = ('id','name','lab__name','group__name','description')

class FlatProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id','name','description')

class ProjectSerializer(ExtensibleSerializer):
    sample_type = ModelRelatedField(model=ModelType,serializer=FlatModelTypeSerializer,required=False,allow_null=True)
    status_options = StatusSerializer(many=True,read_only=True,source='type.status_options')
    lab = ModelRelatedField(model=Lab,serializer=LabSerializer)
    group = ModelRelatedField(model=Group,serializer=GroupSerializer)
    manager = ModelRelatedField(model=User,serializer=FlatUserSerializer,queryset=User.objects.filter(groups__id=1), required=False, allow_null=True)
    participants = ModelRelatedField(model=User,serializer=FlatUserSerializer,many=True,queryset=User.objects.filter(groups__id=1),required=False,allow_null=True)
    related_projects = ModelRelatedField(model=Project,serializer=FlatProjectSerializer,many=True,required=False,allow_null=True)
#     referencing_projects = BasicProjectSerializer(many=True)
    history = JSONField(read_only=True)
    class Meta:
        model = Project
        fields = ('id','type','name','sample_type','data','status_options','lab','group','manager','participants','related_projects','history','project_id','created','description','archived','status')
#         fields = ('id','name','type','type__name','sample_type','description','lab','lab__name','data','created','status','history','status_options','referencing_projects','related_projects','group','participants','manager')

class SampleSerializer(ExtensibleSerializer):
    project = ModelRelatedField(model=Project,serializer=FlatProjectSerializer)
    class Meta:
        model = Sample
        read_only_fields = ('sample_id',)
#         fields = ('id','sample_id','project_id','name','description','project'lab','lab__name','data')
#         fields = ('id','sample_id','project_id','name','description','project__name')

class PoolSerializer(ExtensibleSerializer):
    sample_data = DictField(default={},required=False)
    group = ModelRelatedField(model=Group,serializer=GroupSerializer)
    class Meta:
        model = Pool

class JobSerializer(serializers.ModelSerializer):
    data = JSONField()
    params = JSONField()
    args = JSONField()
    class Meta:
        model = Job
        fields = ('id','job_id','template','params','created','run_at','args','status','data')



from rest_framework import serializers
from glims.lims import Project, Sample, ModelType, Pool, Lab#, File, Note
# from glims.jobs import Job, JobSubmission
from django_compute.models import Job

from jsonfield import JSONField
from glims.models import Status, StatusOption
from django.contrib.auth.models import User
# from rest_framework.fields import WritableField

class JSONWritableField(serializers.Field):
    """
    DRF JSON Field
    """
#     def from_native(self, value):
#         import json
#         print value.replace(':','$')
#         if value:
#             return json.dumps(value)#JSONField(value)
#         else:
#             return None
# 
    def to_internal_value(self,value):
        import json
        if not isinstance(value, str) or value is None:
            return value
        value = json.loads(value)#JSONField(value)
        return value
    def to_representation(self, value):
        return value
        import json
        return json.dumps(value)
#     def to_native(self, value):
#         import json
#         if not isinstance(value, str) or value is None:
#             return value
#         value = json.loads(value)#JSONField(value)
#         return value

# class StatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProjectStatus
#         fields = ('status','set_by','timestamp')

class UserSerializer(serializers.ModelSerializer):
#     type = serializers.StringRelatedField(many=False,read_only=True)
#     type__name = serializers.StringRelatedField(source='type.name')
#     data = JSONWritableField()
#     sample_data = JSONWritableField()
    class Meta:
        model = User
        fields = ('id','last_login','first_name','last_name','email','groups')

class StatusOptionSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="status.id")
    name = serializers.CharField(source="status.name")
    class Meta:
        model = StatusOption
        fields = ('id','name','order')   

class ProjectSerializer(serializers.ModelSerializer):
    lab__name = serializers.CharField(source='lab.name')
    type = serializers.StringRelatedField(many=False,read_only=True)
    status_options = StatusOptionSerializer(many=True,read_only=True,source='type.status_options')
    data = JSONWritableField()
    history = JSONWritableField(read_only=True)
#     history = JSONWritableField()
#     def __init__(self,*args,**kwargs):
#         super(ProjectSerializer,self).__init__(*args,**kwargs)
#         print self.instance.type.status_options
    class Meta:
        model = Project
        fields = ('id','name','type','description','lab','lab__name','data','created','status','history','status_options')
#         depth = 4
#         read_only_fields = ('',)

class SampleSerializer(serializers.ModelSerializer):
#     project = ProjectSerializer(many=False,read_only=True)
#     project_id = serializers.RelatedField(many=False)
#     type = serializers.RelatedField(many=False)
    type__name = serializers.StringRelatedField(source='type.name')
    project__name = serializers.CharField(source='project.name')
    data = JSONWritableField()
    class Meta:
        model = Sample
#         fields = ('id','sample_id','project_id','name','description','project'lab','lab__name','data')
#         fields = ('id','sample_id','project_id','name','description','project__name')

class PoolSerializer(serializers.ModelSerializer):
#     project = ProjectSerializer(many=False,read_only=True)
#     project_id = serializers.RelatedField(many=False)
    type = serializers.StringRelatedField(many=False,read_only=True)
    type__name = serializers.StringRelatedField(source='type.name')
    data = JSONWritableField()
    sample_data = JSONWritableField()
    class Meta:
        model = Pool

# class JobSubmissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = JobSubmission

# class JobSerializer(serializers.ModelSerializer):
#     config = JSONWritableField()
#     args = JSONWritableField()
#     class Meta:
#         model = Job
        

class ModelTypeSerializer(serializers.ModelSerializer):
    content_type__model = serializers.CharField(source='content_type.model')
    class Meta:
        model = ModelType
        field=('name','description','fields','content_type__model')
        
# class FileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = File
#         
# class NoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Note
        
class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        
class JobSerializer(serializers.ModelSerializer):
    data = JSONWritableField()
    params = JSONWritableField()
    args = JSONWritableField()
#     urls = serializers.SerializerMethodField()
#     def get_urls(self,obj):
#         return {'update'}
    class Meta:
        model = Job
        fields = ('id','job_id','template','params','created','run_at','args','status','data')
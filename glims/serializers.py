from rest_framework import serializers
from glims.lims import Project, Sample, ModelType, Pool, Workflow#, File, Note
from glims.jobs import Job, JobSubmission
from django.contrib.auth.models import Group
from rest_framework_hstore.serializers import HStoreSerializer

from jsonfield import JSONField
from rest_framework.fields import WritableField

class JSONWritableField(WritableField):
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
    def to_native(self, value):
        import json
        if not isinstance(value, str) or value is None:
            return value
        value = json.loads(value)#JSONField(value)
        return value

class ProjectSerializer(serializers.ModelSerializer):
    group = serializers.RelatedField(many=False)
    type = serializers.RelatedField(many=False)
    data = JSONWritableField()
    class Meta:
        model = Project
        fields = ('id','name','type','description','group','data')
#         read_only_fields = ('',)

class SampleSerializer(serializers.ModelSerializer):
#     project = ProjectSerializer(many=False,read_only=True)
#     project_id = serializers.RelatedField(many=False)
    data = JSONWritableField()
    class Meta:
        model = Sample
#         fields = ('id','sample_id','project_id','name','description')

class PoolSerializer(serializers.ModelSerializer):
#     project = ProjectSerializer(many=False,read_only=True)
#     project_id = serializers.RelatedField(many=False)
    data = JSONWritableField()
    sample_data = JSONWritableField()
    class Meta:
        model = Pool

class JobSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSubmission

class JobSerializer(serializers.ModelSerializer):
    config = JSONWritableField()
    args = JSONWritableField()
    class Meta:
        model = Job
        
class WorkflowSerializer(serializers.ModelSerializer):
    data = JSONWritableField()
    class Meta:
        model = Workflow

class ModelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelType
        
# class FileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = File
#         
# class NoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Note
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
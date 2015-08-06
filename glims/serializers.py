from rest_framework import serializers
from glims.lims import Project, Sample, ModelType, Pool, Workflow#, File, Note
from glims.jobs import Job, JobSubmission

from jsonfield import JSONField
from rest_framework.fields import WritableField
from glims.lims import Lab

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
    lab__name = serializers.Field(source='lab.name')
    type = serializers.RelatedField(many=False)
    data = JSONWritableField()
    class Meta:
        model = Project
        fields = ('id','name','type','description','lab','lab__name','data')
#         read_only_fields = ('',)

class SampleSerializer(serializers.ModelSerializer):
#     project = ProjectSerializer(many=False,read_only=True)
#     project_id = serializers.RelatedField(many=False)
    type = serializers.RelatedField(many=False)
    project__name = serializers.Field(source='project.name')
    data = JSONWritableField()
    class Meta:
        model = Sample
#         fields = ('id','sample_id','project_id','name','description','project__name')

class PoolSerializer(serializers.ModelSerializer):
#     project = ProjectSerializer(many=False,read_only=True)
#     project_id = serializers.RelatedField(many=False)
    type = serializers.RelatedField(many=False)
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
    content_type__name = serializers.Field(source='content_type.name')
    class Meta:
        model = ModelType
        
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
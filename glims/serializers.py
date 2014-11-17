from rest_framework import serializers
from glims.lims import Project, Sample, Experiment#, File, Note
from django.contrib.auth.models import Group
class ProjectSerializer(serializers.ModelSerializer):
    group = serializers.RelatedField(many=False)
    type = serializers.RelatedField(many=False)
    class Meta:
        model = Project
        fields = ('id','name','type','description','group')
#         read_only_fields = ('',)

class SampleSerializer(serializers.ModelSerializer):
#     project = ProjectSerializer(many=False,read_only=True)
#     project_id = serializers.RelatedField(many=False)
    class Meta:
        model = Sample
#         fields = ('id','sample_id','project_id','name','description')
        
class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        
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
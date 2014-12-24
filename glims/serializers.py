from rest_framework import serializers
from glims.lims import Project, Sample, Experiment, ModelType#, File, Note
from django.contrib.auth.models import Group
from rest_framework_hstore.serializers import HStoreSerializer


class ProjectSerializer(HStoreSerializer):
    group = serializers.RelatedField(many=False)
    type = serializers.RelatedField(many=False)
    class Meta:
        model = Project
        fields = ('id','name','type','description','group')
#         read_only_fields = ('',)
        exclude = ('refs',)

class SampleSerializer(HStoreSerializer):
#     project = ProjectSerializer(many=False,read_only=True)
#     project_id = serializers.RelatedField(many=False)
    class Meta:
        model = Sample
        exclude = ('refs',)
#         fields = ('id','sample_id','project_id','name','description')
        
class ExperimentSerializer(HStoreSerializer):
    class Meta:
        model = Experiment
        exclude = ('refs',)
        
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
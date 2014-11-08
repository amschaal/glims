from rest_framework import serializers
from glims.lims import Study, Sample, Experiment, File, Note
from django.contrib.auth.models import Group
class StudySerializer(serializers.ModelSerializer):
    group = serializers.RelatedField(many=False)
    class Meta:
        model = Study
        fields = ('id','name','description','group')
#         read_only_fields = ('',)

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        
class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
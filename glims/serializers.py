from rest_framework import serializers
from glims.lims import Study, Sample, Experiment, File, Note
class StudySerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
#         fields = ('id',)
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
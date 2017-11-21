from rest_framework import serializers
from proteomics.models import FastaFile, ParameterFile

class FastaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FastaFile
        fields = '__all__'
class ParameterFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParameterFile
        fields = '__all__'
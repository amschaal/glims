from rest_framework import serializers
from proteomics.models import FastaFile, ParameterFile

class FastaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FastaFile
#         fields = ('id','sample_id','project_id','name','description')
        
class ParameterFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParameterFile
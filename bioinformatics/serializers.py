from rest_framework import serializers
from bioinformatics.models import BioinfoProject
from glims.serializers import ProjectSerializer, UserSerializer

class BioinfoProjectSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True,many=False)
    assigned_to = UserSerializer(read_only=True,many=False)
    class Meta:
        model = BioinfoProject
        fields = ('id','project','created','assigned_to','description')
        

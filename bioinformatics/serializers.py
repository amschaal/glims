from rest_framework import serializers
from bioinformatics.models import BioinfoProject
from glims.serializers import ProjectSerializer, UserField
from django.contrib.auth.models import User


class BioinfoProjectSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True,many=False)
    assigned_to = UserField(queryset=User.objects.filter(groups__id=1))
    class Meta:
        model = BioinfoProject
        fields = ('id','project','created','assigned_to','description')

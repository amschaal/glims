from rest_framework import serializers
from bioshare.models import LabShare, ProjectShare

class LabShareSerializer(serializers.ModelSerializer):
    directory = serializers.CharField(read_only=True)
    class Meta:
        model = LabShare

class ProjectShareSerializer(serializers.ModelSerializer):
    directory = serializers.CharField(read_only=True)
    class Meta:
        model = ProjectShare


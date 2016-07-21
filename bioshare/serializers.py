from rest_framework import serializers
from bioshare.models import LabShare, ProjectShare

class LabShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabShare

class ProjectShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectShare


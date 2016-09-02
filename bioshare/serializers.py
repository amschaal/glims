from rest_framework import serializers
from bioshare.models import ProjectShare

class ProjectShareSerializer(serializers.ModelSerializer):
    directory = serializers.CharField(read_only=True)
    real_files = serializers.JSONField(read_only=True)
    symlinks = serializers.JSONField(read_only=True)
    url = serializers.CharField(read_only=True)
    class Meta:
        model = ProjectShare
#         read_only_fields = ('project','labshare','directory')

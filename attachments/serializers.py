from rest_framework import serializers
from models import File, Note
        
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note

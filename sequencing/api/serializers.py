from rest_framework import serializers
from sequencing.models import Machine, Lane, Run
from glims.api.fields import ModelRelatedField
from glims.models import Pool, Library, Lab
from glims.api.serializers import FlatLibrarySerializer, LibrarySerializer,\
    SampleSerializer, AdapterSerializer, PoolSerializer
from django.db import transaction

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine

class RunPoolSerializer(serializers.ModelSerializer):
    libraries = FlatLibrarySerializer(many=True,read_only=True)
    class Meta:
        model = Pool

class RunLaneSerializer(serializers.ModelSerializer):
    pool = ModelRelatedField(model=Pool,serializer=RunPoolSerializer)
    id = serializers.IntegerField(required=False) #Need this otherwise it won't show up in validated data when updating a run
    class Meta:
        model = Lane
        read_only_fields = ('run',)
        extra_kwargs = {'run': {'required': 'False'},'id':{'required':'False'}}
        validators = []  # Remove default global validators

class RunSerializer(serializers.ModelSerializer):
    machine = ModelRelatedField(model=Machine,serializer=MachineSerializer)
    lanes = RunLaneSerializer(many=True,read_only=False,required=False)
    class Meta:
        model = Run
    def validate(self,data):
        keys = []
        for l in data.get('lanes',[]):
            index = l.get('index',None)
            if index in keys:
                raise serializers.ValidationError('Lane indexes must be unique.')
            keys.append(index)
        return data
    def create(self, validated_data):
        lanes_data = validated_data.pop('lanes',[])
        with transaction.atomic():
            run = super(RunSerializer,self).create(validated_data)
            for l in lanes_data:
                Lane.objects.create(run=run, **l)
        return run
    def update(self, instance, validated_data):
        lanes_data = validated_data.pop('lanes',[])
        with transaction.atomic():
            run = super(RunSerializer,self).update(instance,validated_data)
            for l in lanes_data:
                print l
                id = l.pop('id',None)
                if not id:
                    Lane.objects.create(run=run, **l)
                else:
                    lane = Lane.objects.get(id=id)
                    lane_serializer = RunLaneSerializer(lane,data=l)
                    if lane_serializer.is_valid():
                        lane_serializer.save()
                    else:
                        print lane_serializer.errors
            return run

# class LibraryDetailSerializer(serializers.ModelSerializer):
#     sample = SampleSerializer()
#     adapter = AdapterSerializer()
#     class Meta:
#         model = Library
# class RunPoolDetailSerializer(serializers.ModelSerializer):
#     libraries = LibraryDetailSerializer(many=True,read_only=True)
#     class Meta:
#         model = Pool
class RunLaneDetailSerializer(RunLaneSerializer):
#     pool = ModelRelatedField(model=Pool,serializer=RunPoolDetailSerializer)
    pool = ModelRelatedField(model=Pool,serializer=PoolSerializer,required=False,allow_null=True)

class RunDetailSerializer(RunSerializer):
    def __init__(self,*args,**kwargs):
        print "RUN DETAIL SERIALIZER"
        super(RunDetailSerializer, self).__init__(*args,**kwargs)
    lanes = RunLaneDetailSerializer(many=True,read_only=False,required=False)
from rest_framework import serializers
from sequencing.models import Machine, Lane, Run
from glims.api.fields import ModelRelatedField
from glims.models import Pool
from glims.api.serializers import FlatPoolSerializer
from django.utils.functional import empty

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine

class LaneSerializer(serializers.ModelSerializer):
    pool = ModelRelatedField(model=Pool,serializer=FlatPoolSerializer)
    id = serializers.IntegerField(required=False)#serializers.ModelField(model_field=Lane()._meta.get_field('id'))
    class Meta:
        model = Lane
#         fields=('id','pool','description','run')
        read_only_fields = ('run',)
        extra_kwargs = {'run': {'required': 'False'},'id':{'required':'False'}}
        validators = []  # Remove a default "unique together" constraint.
#     def get_validation_exclusions(self):
#         exclusions = super(LaneSerializer, self).get_validation_exclusions()
#         return exclusions + ['run']

def unique_lane_index_validator(lanes):
    print "LANES"
    print lanes
    keys = []
    for l in lanes:
        print l
        index = l.get('index',None)
        if index in keys:
            raise serializers.ValidationError('Lane indexes must be unique.')
        keys.append(index)

class RunSerializer(serializers.ModelSerializer):
    machine = ModelRelatedField(model=Machine,serializer=MachineSerializer)
    lanes = LaneSerializer(many=True,read_only=False)
    class Meta:
        model = Run
    def create(self, validated_data):
        lanes_data = validated_data.pop('lanes')
        run = super(RunSerializer,self).create(validated_data)
        for l in lanes_data:
            Lane.objects.create(run=run, **l)
        return run
#     def run_validation(self,data=empty):
#         print "Run validation"
#         print data
#         unique_lane_index_validator(data.get('lanes',[]))
#         value = super(RunSerializer,self).run_validation(data=data)
#         print value
#         return value
    def update(self, instance, validated_data):
#         lanes_data = validated_data.pop('lanes')
#         run = Run.objects.create(**validated_data)
#         for l in lanes_data:
#             Lane.objects.create(run=run, **l)
        print "!!!!!!!!!!!!!!!!!!"
        print validated_data
        lanes_data = validated_data.pop('lanes')
        run = super(RunSerializer,self).update(instance,validated_data)
        print "???????????????????"
        for l in lanes_data:
            print l
            id = l.pop('id',None)
            if not id:
                Lane.objects.create(run=run, **l)
            else:
                lane = Lane.objects.get(id=id)
                lane_serializer = LaneSerializer(lane,data=l)
                if lane_serializer.is_valid():
#                     print 'VALID!!!'
#                     print lane_serializer.data
                    lane_serializer.save()
                else:
                    print lane_serializer.errors
#                 Lane.objects.filter(id=run).update(**l)
        return run
        
        
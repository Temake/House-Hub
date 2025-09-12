from rest_framework import serializers
from .models import house

class HouseAppSerializers(serializers.ModelSerializer):
    members_count = serializers.IntegerField(default=0,read_only=True)
    members=serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='profile-detail')
    manager= serializers.HyperlinkedRelatedField(many=False,read_only=True,view_name='profile-detail')
    taskList= serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='tasklist-detail',source='lists')
    
    class Meta:
        model = house
        fields= ['url','id','name','created_on','members','manager','members_count','description',
                 'completed_task_count','points','non_completed_task_count','taskList']
        read_only_fields = ['points','completed_task_count','non_completed_task_count']
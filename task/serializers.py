from .models import TaskList,Task,Atttachments

from rest_framework import serializers,status

from house.models import house

class TaskListApp(serializers.ModelSerializer):
    house=serializers.HyperlinkedRelatedField(many=False,queryset=house.objects.all(),view_name='house-detail')
    created_by=serializers.HyperlinkedRelatedField(many=False,read_only= True,view_name='house-detail')
    tasks=serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='task-detail')
    class Meta:
        model= TaskList
        fields=['url','id','title','created_on','created_by','description','status','house','tasks',]
        read_only_fields=['created_on','status']
class TaskApp(serializers.ModelSerializer):
    completed_by=serializers.HyperlinkedRelatedField(many=False,read_only= True,view_name='profile-detail')
    created_by=serializers.HyperlinkedRelatedField(many=False,read_only= True,view_name='profile-detail')
    task_list=serializers.HyperlinkedRelatedField(many=False,queryset=TaskList.objects.all(),view_name='tasklist-detail')
    attachments=serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='atttachments-detail')

    
    
    def validate_task_list(self,value):
        user_profile=self.context['request'].user.profile
        if value not in user_profile.house.lists.all():
            raise serializers.ValidationError("You are not a member of the house with this list")
        return value
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.task_list = validated_data.get('task_list', instance.task_list)
        instance.save()
        return instance
    
    def create(self, validated_data):
        user_profile=self.context['request'].user.profile
        task=Task.objects.create(**validated_data)
        task.created_by=user_profile
        task.save()
        return task

    class Meta:
        model= Task
        fields=['url','id','title','created_on','created_by','completed_by','status','description','task_list','attachments']
        read_only_fields=['created_on','created_by','status','completed_by',]
class Attachments(serializers.ModelSerializer):
    task= serializers.HyperlinkedRelatedField(many=False,queryset=Task.objects.all(),view_name='task-detail')
    
    
    def validate_task(self,value):
            user_profile=self.context['request'].user.profile
            if value.task_list not in user_profile.house.lists.all():
                raise serializers.ValidationError({"taskt":"You are not a member of the house with this list"},status.HTTP_400_BAD_REQUEST)
            return value
    class Meta:
        model= Atttachments
        fields=['url','id','task','file','created_on']
        read_only_fields=['created_on']
        
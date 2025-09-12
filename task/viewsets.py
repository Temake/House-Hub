from .models import Task,TaskList,Atttachments
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.utils import timezone
from rest_framework.decorators import action
from rest_framework import viewsets,mixins,response,status,filters
from rest_framework import status as s
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import COMPLETED,NOT_COMPLETED
from .serializers import TaskApp,TaskListApp,Attachments
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsallowedtoEditTaskList,IsAllowedToEditTask,IsAllowedtoEditAttachment


@extend_schema_view(
    create=extend_schema(tags=['Tasks'], summary='Create a new task list'),
    retrieve=extend_schema(tags=['Tasks'], summary='Get task list details'),
    update=extend_schema(tags=['Tasks'], summary='Update task list'),
    partial_update=extend_schema(tags=['Tasks'], summary='Partially update task list'),
    destroy=extend_schema(tags=['Tasks'], summary='Delete task list')
)
class TaskListviewset(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    serializer_class=TaskListApp
    queryset=TaskList.objects.all()
    permission_classes=[IsallowedtoEditTaskList]
    def get_queryset(self):
        user_house=self.request.user.profile.house
        return TaskList.objects.filter(house=user_house)
    def created_by(self,serializers):
        us=self.request.user
        if serializers.is_valid():
            serializers.save(created_by=us)
        else:
            print(serializers.errors)
        

      
    

@extend_schema_view(
    list=extend_schema(tags=['Tasks'], summary='List all tasks'),
    create=extend_schema(tags=['Tasks'], summary='Create a new task'),
    retrieve=extend_schema(tags=['Tasks'], summary='Get task details'),
    update=extend_schema(tags=['Tasks'], summary='Update task'),
    partial_update=extend_schema(tags=['Tasks'], summary='Partially update task'),
    destroy=extend_schema(tags=['Tasks'], summary='Delete task'),
    update_task_status=extend_schema(tags=['Tasks'], summary='Update task status')
)
class TaskViewset(viewsets.ModelViewSet):
    serializer_class=TaskApp
    queryset=Task.objects.all()
    permission_classes=[IsAllowedToEditTask] 
    filter_backends= [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields=['name','status']
    filterset_fields=['status',]
    
    def get_queryset(self):
        query_set=super(TaskViewset,self).get_queryset()
        user_profile=self.request.user.profile
        updated_query_set=query_set.filter(created_by=user_profile)
        return updated_query_set
    @action(detail=True,methods=['patch','put'])
    def update_task_status(self,request,pk=None):
        try:
            task=self.get_object()
            profile=self.request.user.profile
            status= request.data['status']
            if status == NOT_COMPLETED:
                if task.status == COMPLETED:
                    task.status=NOT_COMPLETED
                    task.completed_by=None
                    task.completed_on=None
            elif status == COMPLETED:
                if task.status == NOT_COMPLETED:
                    task.status=COMPLETED
                    task.completed_by=profile
                    task.completed_on=timezone.now()
            task.save()
            serializers = TaskApp(instance=task,context={'request':request})
            return response.Response(serializers.data,status=s.HTTP_200_OK)
        except Exception as e:
            return response.Response({"detail":str(e)},status=s.HTTP_400_BAD_REQUEST)
            
    
@extend_schema_view(
    list=extend_schema(tags=['Tasks'], summary='List all attachments'),
    create=extend_schema(tags=['Tasks'], summary='Create a new attachment'),
    retrieve=extend_schema(tags=['Tasks'], summary='Get attachment details'),
    update=extend_schema(tags=['Tasks'], summary='Update attachment'),
    partial_update=extend_schema(tags=['Tasks'], summary='Partially update attachment'),
    destroy=extend_schema(tags=['Tasks'], summary='Delete attachment')
)
class AttachmentsViewSet(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):

    serializer_class=Attachments
    queryset=Atttachments.objects.all()
    permission_classes=[IsAllowedtoEditAttachment]
    

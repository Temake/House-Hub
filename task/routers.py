from rest_framework import routers
from .viewsets import TaskViewset,TaskListviewset,AttachmentsViewSet
app_name = "task"

router = routers.DefaultRouter()

router.register('task',TaskViewset)
router.register('task-list',TaskListviewset)
router.register('attachments',AttachmentsViewSet)
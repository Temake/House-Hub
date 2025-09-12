from django.contrib import admin
from .models import Task,TaskList,Atttachments

# Register your models here.
admin.site.register(Task)
admin.site.register(TaskList)
admin.site.register(Atttachments)


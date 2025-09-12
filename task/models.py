from django.db import models
import uuid
from django.utils.deconstruct import deconstructible

import os
@deconstructible
class GenerateAttachmentsFilepath(object):
    def __init__(self):
        pass
        
    def __call__(self, instance, filename):
        ext= filename.split('.')[-1]
        path= f'media/task/{str(instance.task.id)}/attachments/'
        name=f'{instance.id}.{ext}'
        return os.path.join(path, name)
attachment = GenerateAttachmentsFilepath()
        
# Create your models here.
NOT_COMPLETED = 'NC'
COMPLETED='C'
TASK_CHOICES = (
    (NOT_COMPLETED, 'Not Completed'),
    (COMPLETED, 'Completed'),
)
class TaskList(models.Model):
    title= models.CharField(max_length=120)
    completed_on = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by= models.ForeignKey('users.Profile', on_delete=models.SET_NULL,null=True,blank=True, related_name='lists')
    description= models.TextField(null=True,blank=True)
    house= models.ForeignKey('house.house', on_delete=models.CASCADE,null=True,blank=True, related_name='lists')
    status= models.CharField(max_length=2, choices=TASK_CHOICES, default=NOT_COMPLETED)
    def __str__(self):
        return self.title
class Task(models.Model):
    title = models.CharField(max_length=200)
    completed_on = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    task_list= models.ForeignKey('task.TaskList', on_delete=models.CASCADE, related_name='tasks')
    created_by= models.ForeignKey('users.Profile', on_delete=models.SET_NULL,null=True,blank=True, related_name='created_task')
    completed_by= models.ForeignKey('users.Profile', on_delete=models.SET_NULL,null=True,blank=True, related_name='completed_task')
    status= models.CharField(max_length=2, choices=TASK_CHOICES, default=NOT_COMPLETED)
    description= models.TextField(null=True,blank=True)

    def __str__(self):
        return f'{self.id} | {self.title}'
    
class Atttachments(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task= models.ForeignKey('task.Task', on_delete=models.CASCADE, related_name='attachments')
    file= models.FileField(upload_to=attachment)
    created_on= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.id} | {self.task}'
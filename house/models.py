from django.db import models
import uuid
import os
from django.utils.deconstruct import deconstructible
from django.core.validators import FileExtensionValidator

# Create your model
@deconstructible
class Genimg(object):
    def __init__(self):
        pass
    
    def __call__(self, instance, filename):
        if '.' not in filename:
            raise ValueError("Filename must have an extension.")
        ext= filename.split('.')[-1]
        path= f'media/houses/{str(instance.id)}/images/'
        unique_name = f'main_{str(uuid.uuid4().hex)}.{ext}'
        return os.path.join(path, unique_name)
pics=Genimg()

class house(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name= models.CharField(max_length=100)
    #img= models.ImageField(upload_to=pics,blank=True,null=True ,validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])
    created_on= models.DateTimeField(auto_now_add=True)
    description=models.TextField()
    manager=models.OneToOneField('users.Profile',on_delete=models.SET_NULL,null=True,blank=True,related_name='managed_house')
    completed_task_count= models.IntegerField(default=0)
    points=models.IntegerField(default=0)
    non_completed_task_count= models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.name} | created on {self.created_on}'
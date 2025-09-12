from django.db import models
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
import os

# Create your models here.
@deconstructible
class Genimg(object):
    def __init__(self) -> None:
        pass
        
    def __call__(self, instance,filename):
        ext = filename.split('.')[-1]
        path = f'media/accounts/{str(instance.user.id)}/images/'
        name= f'profile_image.{ext}'
        return os.path.join(path,name)
user_profile_image_path=Genimg()

         

class Profile(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    img= models.ImageField(upload_to=user_profile_image_path, null=True, blank=True)
    house=models.ForeignKey('house.house',on_delete=models.SET_NULL,null=True,blank=True,related_name='members')

    def __str__(self):
        return f'{self.user.username}\'s profile'
    
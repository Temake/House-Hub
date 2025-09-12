from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from .models import Profile
from django.dispatch import receiver

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(pre_save, sender=User)
def set_username(sender, instance, **kwargs):
    if not instance.username:
        if instance.first_name and instance.last_name:
            username = f'{instance.first_name}_{instance.last_name}'
            counter= 1
        elif instance.first_name and not instance.last_name:
            username= instance.first_name
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f'{username}_{counter}'
                counter += 1
            instance.username = username
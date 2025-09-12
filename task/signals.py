from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import Task,NOT_COMPLETED,COMPLETED
@receiver(post_save,sender=Task)
def increase_points(sender,instance,created,**kwargs):
    print("Signal received for Task status change")
    house=instance.task_list.house
    if instance.status == COMPLETED:
        house.points += 10
    elif instance.status == NOT_COMPLETED:
        if house.points >= 10:
            house.points-= 10
    house.save()
@receiver(post_save,sender=Task)
def status_change(sender,instance,created,**kwargs):
    task_list=instance.task_list
    is_completed=True
    for task in task_list.tasks.all():
        if task.status == NOT_COMPLETED:
            is_completed=False
    if is_completed:
        task_list.status=COMPLETED
    else:
        task_list.status=NOT_COMPLETED
    task_list.save()
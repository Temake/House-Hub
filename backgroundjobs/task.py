
# # Check if the task exists before creating a new one
# from background_task import background
# from background_task.tasks import Task as bt

# from task.models import COMPLETED
# from house.models import house

# @background(schedule=10)
# def calculate_house_stats():
#     for houses in house.objects.all():
#         total_task = 0
#         completed_tasks_count = 0
#         house_tasks_list = houses.lists.all()
#         for tasks in house_tasks_list:
#             total_task += tasks.tasks.count()
#             completed_tasks_count += tasks.tasks.filter(status=COMPLETED).count()
#         houses.completed_task_count = completed_tasks_count
#         houses.non_completed_task_count = total_task - completed_tasks_count
#         houses.save()

# # Check if the task exists before creating a new one
# if not bt.objects.filter(verbose_name='calculate_house_stats').exists():
#     calculate_house_stats(repeat=bt.DAILY, verbose_name='calculate_house_stats', priority=0)

    
    
import os
import django
from unicodedata import category

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_proj.settings')
django.setup()


# Задание 1. Создание записей:

from task_manager.models import Task, SubTask, Category
from datetime import datetime, timedelta
from django.utils import timezone


category = Category.objects.bulk_create([
    Category(name="Auto"),
    Category(name="Home"),
    Category(name="Electronics"),
])

task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    status="New",
    deadline=timezone.now()  + timedelta(days=3)
)


print("Task created")
print(f'Title: {task.title}, status: {task.status}')


subtask = SubTask.objects.bulk_create([
    SubTask(
        task=task,
        title="Gather information",
        description="Find necessary information for the presentation",
        status="New",
        deadline=timezone.now()  + timedelta(days=2)
    ),
    SubTask(
        task=task,
        title="Create slides",
        description="Create presentation slides",
        status="New",
        deadline=timezone.now()  + timedelta(days=1)
    ),

# Дополнительно для пункта 2 на чтение:
    SubTask(
            task=task,
            title="Info",
            description="Add description",
            status="Done",
            deadline=timezone.now()  - timedelta(days=3)
        ),
    SubTask(
            task=task,
            title="Availability",
            description="Check availability in stock",
            status="Done",
            deadline=timezone.now()  - timedelta(days=1)
        ),
])
print("Subtask created")



# Задание 2. Чтение записей:

new_tasks = Task.objects.filter(status="New")

for task in new_tasks:
    print(f'Task wits status "New": {task.title}, Deadline: {task.deadline}')


done_subtasks = SubTask.objects.filter(
    status="Done",
    deadline__lt=timezone.now()
)

for subtask in done_subtasks:
    print(f'Subtask wits status "Done": {subtask.title}, Deadline: {subtask.deadline}')



# Задание 3. Изменение записей:

change_task = Task.objects.get(title="Prepare presentation")
change_task.status = "In Progress"
change_task.save()

deadline_subtask = SubTask.objects.get(title="Gather information")
deadline_subtask.deadline = timezone.now() - timedelta(days=2)
deadline_subtask.save()

description_subtask = SubTask.objects.get(title="Create slides")
description_subtask.description = "Create and format presentation slides"
description_subtask.save()



# Задание 4. Удаление записей:

# delete_task = Task.objects.get(title="Prepare presentation")
# delete_task.delete()



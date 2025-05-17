import random
import sys
import os
from datetime import timezone

import django
from faker import Faker

# Добавление пути к внутренней папке проекта
sys.path.append('C:\\Users\\yuniz\\Desktop\\DjangoLessons')  # Путь к папке с settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_proj.settings')
django.setup()

# Теперь безопасно импортировать модели
from django.contrib.auth.models import User
from task_manager.models import Task, SubTask

fake = Faker()

def generate_test_data():
    try:
        user = User.objects.get(username='testuser')
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )

    num_tasks = random.randint(3, 5)
    for _ in range(num_tasks):
        task = Task.objects.create(
            title=fake.sentence(nb_words=4),
            description=fake.paragraph(nb_sentences=3),
            deadline=fake.future_datetime(end_date="+30d", tzinfo=timezone.utc),
            owner=user
        )
        num_subtasks = random.randint(1, 2)
        for _ in range(num_subtasks):
            SubTask.objects.create(
                task=task,
                title=fake.sentence(nb_words=3),
                description=fake.paragraph(nb_sentences=2),
                deadline=fake.future_datetime(end_date="+15d", tzinfo=timezone.utc),
                owner=user
            )
    print(f"Created {num_tasks} tasks with 1-2 subtasks each for user {user.username}")

if __name__ == "__main__":
    generate_test_data()
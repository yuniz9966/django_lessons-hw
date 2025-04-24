from rest_framework import serializers
from task_manager.models import Task, SubTask, Category
from django.utils import timezone

# HW12. Задание 1: Эндпоинт для создания задачи
# Задача должна быть создана с полями title, description, status, и deadline.
class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']


# HW12.  Задание 2: Эндпоинты для получения списка задач и конкретной задачи по её ID
class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']


class TaskByIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"



# HW 13

# Задание 1: Переопределение полей сериализатора
class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = [
            "id",
            "title",
            "description",
            "task",
            "status",
            "deadline",
            "created_at"
        ]
        read_only_fields = ['created_at',]


# Задание 2: Переопределение методов create и update
class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields= ["name"]

    def validate_name(self, value: str):
        if value:
            unique_name = Category.objects.filter(name__iexact=value).exists()
            if unique_name:
                raise serializers.ValidationError(
                    "Такая категория уже существует!"
                )
        return value


# Задание 3: Использование вложенных сериализаторов
class SubTaskSerializer(serializers.ModelSerializer):
    task = serializers.StringRelatedField()

    class Meta:
        model = SubTask
        fields = "__all__"


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = "__all__"
        # exclude = ['']  # все поля, кроме...


# Задание 4: Валидация данных в сериализаторах
class TaskCreateSerialize(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "categories",
            "deadline"
        ]


    def validate_deadline(self, value: str):
        if value < timezone.now():
            raise serializers.ValidationError(
                f"Дата не может быть меньше {timezone.now()}"
            )
        return value
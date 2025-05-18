import re

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.admin import User

from task_manager.models import Task, SubTask, Category
from django.utils import timezone


# HW20
class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(
        choices=[
            ("ADMIN", "ADMIN"),
            ("MODERATOR", "MODERATOR"),
            ("LIB MEMBER", "LIB MEMBER"),
        ],
        required=False,
    )
    is_staff = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = [
            "username", "first_name",
            "last_name", "password",
            "re_password", "email",
            "role", "is_staff",
        ]

    def validate(self, attrs):
        first_name = attrs.get("first_name")
        last_name = attrs.get("last_name")

        re_pattern = r'^[a-zA-Z]+$'

        if not re.match(re_pattern, first_name):
            raise serializers.ValidationError(
                {"first_name": "First name must contain only alphabet characters"}
            )

        if not re.match(re_pattern, last_name):
            raise serializers.ValidationError(
                {"last_name": "Last name must contain only alphabet characters"}
            )

        password = attrs.get("password")
        re_password = attrs.pop("re_password", None)

        if not password:
            raise serializers.ValidationError(
                {"password": "Password must not be empty"}
            )

        if not re_password:
            raise serializers.ValidationError(
                {"re_password": "Password must not be empty"}
            )

        validate_password(password)

        if password != re_password:
            raise serializers.ValidationError(
                {"re_password": "Password didn't match"}
            )

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)

        user.save()

        return user




# HW12. Задание 1: Эндпоинт для создания задачи
# Задача должна быть создана с полями title, description, status, и deadline.
class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']
        read_only_fields = ['owner']


# HW12.  Задание 2: Эндпоинты для получения списка задач и конкретной задачи по её ID
class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline', 'owner']
        read_only_fields = ['owner']

class TaskByIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ['owner']


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
        read_only_fields = ['created_at', 'owner']



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
        read_only_fields = ['owner']


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = "__all__"
        # exclude = ['']  # все поля, кроме...
        read_only_fields = ['owner']


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
        read_only_fields = ['owner']


    def validate_deadline(self, value: str):
        if value < timezone.now():
            raise serializers.ValidationError(
                f"Дата не может быть меньше {timezone.now()}"
            )
        return value
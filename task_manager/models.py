from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from task_manager.managers.categories import SoftDeleteManager

status_choises = [
        ("New", "New"),
        ("In Progress", "In Progress"),
        ("Pending", "Pending"),
        ("Blocked", "Blocked"),
        ("Done", "Done")
    ]


class Category(models.Model):
    name = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()

        self.save()

    def __str__(self):
        return self.name


    class Meta:
        db_table = "task_manager_category"
        verbose_name = "Category"
        unique_together = ("name",)



class Task(models.Model):
    title = models.CharField(max_length=50, unique_for_date="deadline")
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    status = models.CharField(max_length=100, choices=status_choises)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title


    class Meta:
        db_table = "task_manager_task"
        verbose_name = "Task"
        unique_together = ("title",)
        ordering = ("-created_at",)


class SubTask(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=status_choises)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subtasks')

    def __str__(self):
        return self.title


    class Meta:
        db_table = "task_manager_subtask"
        verbose_name = "SubTask"
        unique_together = ("title",)
        ordering = ("-created_at",)


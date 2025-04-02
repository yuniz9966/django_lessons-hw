from django.contrib import admin

from task_manager.models import Category, Task, SubTask # импорт нужных моделей из нужного приложения

admin.site.register(Category)
admin.site.register(Task)
admin.site.register(SubTask)
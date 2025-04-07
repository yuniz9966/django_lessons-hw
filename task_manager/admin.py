from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from task_manager.models import Category, Task, SubTask # импорт нужных моделей из нужного приложения

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'status')


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'task', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'task', 'status')



# admin.site.register(Category)
# admin.site.register(Task)
# admin.site.register(SubTask)
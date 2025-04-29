from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from first_app.views import django_greetings, django_greetings_2
# from task_manager.views import task_create, task_list, task_detail, task_statistic
from task_manager.views import (
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    SubTaskListCreateView,
    SubTaskRetrieveUpdateDestroyView,
)
from rest_framework.routers import DefaultRouter
from task_manager.views import CategoryViewSet


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)




def redirect_to_admin(request):
    return redirect('/admin/')

urlpatterns = [
    path('', redirect_to_admin),
    path('admin/', admin.site.urls),
    path('greetings/', django_greetings, name='django_greetings'),
    path('greetings_hello/<str:name>', django_greetings_2),

    # path('tasks/create/', task_create),
    # path('tasks/', task_list),
    # path('tasks/<int:task_id>/', task_detail),
    # path('tasks/statistic/', task_statistic),

    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyView.as_view(), name='subtask-detail'),

    path('', include(router.urls))
]




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
    UserTaskListView,
)
from rest_framework.routers import DefaultRouter
from task_manager.views import CategoryViewSet

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title='Tasks API',
        default_version='v1',
        description='Our Tasks API with permissions',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='test.email@gmail.com'),
        license=openapi.License(name='OUR LICENSE', url='https://example.com')
    ),
    public=False,
    permission_classes=[permissions.AllowAny],
)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)


# def redirect_to_admin(request):
#     return redirect('/admin/')

urlpatterns = [
    # path('', redirect_to_admin),
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

    path('', include(router.urls)),

    path('auth-login-jwt/', TokenObtainPairView.as_view()),
    path('token-refresh/', TokenRefreshView.as_view()),

    path('user-task/', UserTaskListView.as_view(), name='user-task'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
]




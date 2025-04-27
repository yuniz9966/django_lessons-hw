from django.db.models import Count, QuerySet
from django.db.models.functions import ExtractWeekDay
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from task_manager.models import Task, SubTask
from task_manager.serializers import (TaskCreateSerialize,
                                      TaskDetailSerializer,
                                      SubTaskCreateSerializer,
                                      SubTaskSerializer)
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from rest_framework.decorators import action

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from task_manager.models import Task, SubTask
from task_manager.serializers import (
    TaskListSerializer,
    TaskCreateSerializer,
    TaskByIDSerializer,
    SubTaskCreateSerializer,
    SubTaskSerializer
)


# HW 15
# Задание 1: Замена представлений для задач (Tasks) на Generic Views
class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskListSerializer


class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = TaskByIDSerializer


# HW 15
# Задание 2: Замена представлений для подзадач (SubTasks) на Generic Views
class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubTaskCreateSerializer
        return SubTaskSerializer


class SubTaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer









# # HW13
# # Задание 5: Создание классов представлений
# class SubTaskListCreateAPIView(APIView, PageNumberPagination):
#     page_size = 5
#
#     def get_queryset(self, request: Request):
#
#         queryset: QuerySet[SubTask] = SubTask.objects.all()
#
#         tasks = request.query_params.getlist('task')
#         status = request.query_params.get('status')
#
#         if tasks:
#             queryset = queryset.filter(task__title__in=tasks)
#
#         if status:
#             valid_statuses = [choice[0] for choice in SubTask.STATUS_CHOICES]
#             if status in valid_statuses:
#                 queryset = queryset.filter(status=status)
#             else:
#                 queryset = queryset.none()
#
#         return queryset.order_by("-created_at")
#
#     def get_page_size(self, request):
#         page_size = request.query_params.get('page_size')
#
#         if page_size and page_size.isdigit():
#             return int(page_size)
#
#         return self.page_size
#
#     def get(self, request: Request) -> Response:
#         subtasks: QuerySet[SubTask] = self.get_queryset(request=request)
#         # subtasks: QuerySet[SubTask] = SubTask.objects.all().order_by("-created_at")
#         results = self.paginate_queryset(queryset=subtasks, request=request, view=self)
#         serializer = SubTaskSerializer(results, many=True)
#         # return Response(data=serializer.data, status=status.HTTP_200_OK)
#         return self.get_paginated_response(data=serializer.data)
#
#     def post(self, request: Request) -> Response:
#         serializer = SubTaskCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class SubTaskDetailUpdateDeleteView(APIView):
#     def get(self, request: Request, **kwargs) -> Response:
#         try:
#             subtask = SubTask.objects.get(id=kwargs['subtask_id'])
#         except SubTask.DoesNotExist:
#             return Response(
#                 data={
#                     "message": "Подзадача не найдена!"
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         serializer = SubTaskSerializer(subtask)
#
#         return Response(
#             data=serializer.data,
#             status=status.HTTP_200_OK
#         )
#
#     def put(self, request: Request, **kwargs) -> Response:
#         try:
#             subtask = SubTask.objects.get(id=kwargs['subtask_id'])
#         except SubTask.DoesNotExist:
#             return Response(
#                 data={
#                     "message": "Подзадача не найдена!"
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )
#
#         serializer = SubTaskCreateSerializer(instance=subtask, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(
#                 data=serializer.data,
#                 status=status.HTTP_200_OK
#             )
#
#         else:
#             return Response(
#                 data=serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#     def delete(self, request: Request, **kwargs) -> Response:
#         try:
#             subtask = SubTask.objects.get(id=kwargs['subtask_id'])
#         except SubTask.DoesNotExist:
#             return Response(
#                 data={
#                     "message": "Подзадача не найдена!"
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )
#
#         subtask.delete()
#
#         return Response(
#             data={
#                 "message": "Книга была успешно удалена."
#             },
#             status=status.HTTP_202_ACCEPTED
#         )
#
#
# def user_hello1(request):
#     return HttpResponse(
#         f"<h1>Hello, Prog2!!! :)</h1>"
#     )
#
#
# class TaskListCreateAPIView(APIView):
#     WEEKDAY_MAP = {
#         'воскресенье': 1,
#         'sunday': 1,
#         'понедельник': 2,
#         'monday': 2,
#         'вторник': 3,
#         'tuesday': 3,
#         'среда': 4,
#         'wednesday': 4,
#         'четверг': 5,
#         'thursday': 5,
#         'пятница': 6,
#         'friday': 6,
#         'суббота': 7,
#         'saturday': 7,
#     }
#
#     def get_queryset(self, request: Request) -> QuerySet[Task]:
#         queryset: QuerySet[Task] = Task.objects.all()
#         day_of_week = request.query_params.get("weekday")
#
#         if day_of_week:
#             if day_of_week not in self.WEEKDAY_MAP:
#                 raise ValidationError("Неверный день недели!")
#
#             weekday_num = self.WEEKDAY_MAP.get(day_of_week.lower())
#             queryset = queryset.annotate(weekday=ExtractWeekDay('deadline')).filter(weekday=weekday_num)
#
#         return queryset
#
#     def get(self, request: Request) -> Response:
#         tasks = self.get_queryset(request=request)
#         serializer = TaskDetailSerializer(tasks, many=True)
#
#         return Response(
#             data=serializer.data,
#             status=status.HTTP_200_OK
#         )
#
#     def post(self, request: Request) -> Response:
#         serializer = TaskCreateSerialize(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# # @api_view(['POST'])
# # def tasks_create(request: Request) -> Response:
# #     serializer = TaskCreateSerialize(data=request.data)
# #
# #     if serializer.is_valid():
# #         serializer.save()
# #         return Response(serializer.data, status=status.HTTP_201_CREATED)
# #     else:
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
#
# # @api_view(['GET'])
# # def list_of_tasks(request) -> Response:
# #     tasks = Task.objects.all()
# #     serializer = TaskDetailSerializer(tasks, many=True)
# #
# #     return Response(
# #         data=serializer.data,
# #         status=status.HTTP_200_OK
# #     )
#
# @api_view(['GET'])
# def get_task_by_id(request, task_id: int) -> Response:
#     try:
#         task = Task.objects.get(id=task_id)
#     except Task.DoesNotExist:
#         return Response(
#             data={
#                 "message": "TASK NOT FOUND"
#             },
#             status=404
#         )
#
#     serializer = TaskDetailSerializer(task)
#
#     return Response(
#         data=serializer.data,
#         status=200
#     )
#
#
# @api_view(['GET'])
# def tasks_count(request) -> Response:
#     tasks_cn = Task.objects.count()
#
#     return Response(data=f"{tasks_cn=}", status=status.HTTP_200_OK)
#
#
# class TaskStatusCountSerializer:
#     pass
#
#
# @api_view(['GET'])
# def tasks_count_by_status(request) -> Response:
#     statuses_count_by_task = Task.objects.values("status").annotate(Count("id"))
#     serializer = TaskStatusCountSerializer(statuses_count_by_task, many=True)
#     return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['GET'])
# def tasks_of_overdue(request) -> Response:
#     count_of_overdue_task = Task.objects.filter(deadline__lt=timezone.now()).count()
#
#     return Response(data=f"{count_of_overdue_task=}", status=status.HTTP_200_OK)
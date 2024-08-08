from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Task, TaskCategory, UserTask, ensure_user_tasks
from .serializers import TaskCategorySerializer, TaskSerializer, UserTaskSerializer
from rest_framework.views import APIView
from django_filters import rest_framework as filters

class TaskFilter(filters.FilterSet):
    category = filters.NumberFilter(field_name="category__id")
    
    class Meta:
        model = Task
        fields = ['category']

class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilter

class UserTaskFilter(filters.FilterSet):
    category = filters.NumberFilter(field_name="task__category__id")
    completed = filters.BooleanFilter(field_name="completed")
    
    class Meta:
        model = UserTask
        fields = ['category', 'completed']

class UserTaskViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserTaskSerializer
    filterset_class = UserTaskFilter

    def get_queryset(self):
        ensure_user_tasks(self.request.user)
        return UserTask.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        user_task = self.get_object()
        if user_task.completed:
            return Response({"detail": "Task already completed."}, status=status.HTTP_400_BAD_REQUEST)
        
        user_task.completed = True
        user_task.completed_at = timezone.now()
        user_task.save()
        
        # Update user balance
        user = request.user
        user.balance += user_task.task.rewards
        user.save()
        
        return Response({"detail": "Task completed successfully.", "points_earned": user_task.task.rewards})

class TaskCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskCategory.objects.all()
    serializer_class = TaskCategorySerializer


class EnsureUserTasksView(APIView):
    def post(self, request):
        ensure_user_tasks(request.user)
        return Response({"detail": "User tasks have been updated."}, status=status.HTTP_200_OK)
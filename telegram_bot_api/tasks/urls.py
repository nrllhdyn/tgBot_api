from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnsureUserTasksView, TaskViewSet, UserTaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'user-tasks', UserTaskViewSet, basename='user-task')

urlpatterns = [
    path('', include(router.urls)),
    path('ensure-user-tasks/', EnsureUserTasksView.as_view(), name='ensure-user-tasks'),
]
from rest_framework import serializers
from .models import Task, TaskCategory, UserTask

class TaskCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCategory
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'name', 'link', 'rewards', 'category', 'category_name']

class UserTaskSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)
    
    class Meta:
        model = UserTask
        fields = ['id', 'task', 'completed', 'completed_at']
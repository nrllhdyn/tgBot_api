from django.contrib import admin
from .models import Task, TaskCategory, UserTask


@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'rewards')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(UserTask)
class UserTaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'completed', 'completed_at')
    list_filter = ('completed', 'task__category')
    search_fields = ('user__username', 'task__name')
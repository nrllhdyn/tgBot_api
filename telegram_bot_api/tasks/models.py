from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

class TaskCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Task Categories"

class Task(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    rewards = models.PositiveIntegerField(default=50)
    category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE, related_name='tasks')
    
    def __str__(self):
        return self.name

class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tasks')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'task')
    
    def __str__(self):
        return f"{self.user.username} - {self.task.name}"

def ensure_user_tasks(user):
    existing_tasks = UserTask.objects.filter(user=user).values_list('task_id', flat=True)
    all_tasks = Task.objects.exclude(id__in=existing_tasks)
    
    new_user_tasks = [UserTask(user=user, task=task) for task in all_tasks]
    UserTask.objects.bulk_create(new_user_tasks)

@receiver(post_save, sender=Task)
def create_user_tasks(sender, instance, created, **kwargs):
    if created:
        users = User.objects.all()
        user_tasks = [UserTask(user=user, task=instance) for user in users]
        UserTask.objects.bulk_create(user_tasks)

@receiver(post_save, sender=User)
def create_tasks_for_new_user(sender, instance, created, **kwargs):
    if created:
        ensure_user_tasks(instance)
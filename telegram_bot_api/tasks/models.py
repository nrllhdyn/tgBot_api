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
    category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE,related_name='tasks')
    
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
    
@receiver(post_save, sender=Task)
def create_user_tasks(sender, instance, created, **kwargs):
    if created:
        users = User.objects.all()
        for user in users:
            UserTask.objects.create(user=user, task=instance)
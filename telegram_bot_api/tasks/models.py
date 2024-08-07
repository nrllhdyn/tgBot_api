from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    reward = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField()
    
    def __str__(self):
        return self.name
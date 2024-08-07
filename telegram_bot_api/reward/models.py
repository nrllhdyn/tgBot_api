from django.db import models

class DailyReward(models.Model):
    day = models.PositiveIntegerField(unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Day {self.day}: {self.amount}"
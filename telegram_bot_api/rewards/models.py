from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class DailyReward(models.Model):
    day = models.PositiveIntegerField(unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Day {self.day}: {self.amount}"

class UserDailyReward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_rewards')
    day = models.PositiveIntegerField()
    claimed_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('user', 'day')

    def __str__(self):
        return f"{self.user.username} - Day {self.day}: {self.amount}"
from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    is_referral_bonus = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'day', 'is_referral_bonus')

    def __str__(self):
        return f"{self.user.username} - Day {self.day}: {self.amount}"

@receiver(post_save, sender=UserDailyReward)
def give_referrer_bonus(sender, instance, created, **kwargs):
    if created and not instance.is_referral_bonus:
        referrer = instance.user.by_referred
        if referrer:
            bonus_amount = Decimal(instance.amount) * Decimal('0.05')
            
            UserDailyReward.objects.create(
                user=referrer,
                day=instance.day,
                amount=bonus_amount,
                is_referral_bonus=True
            )
            
            referrer.balance += bonus_amount
            referrer.save()
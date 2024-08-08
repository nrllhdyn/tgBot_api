from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from referrals.models import Referral
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
    is_referral_reward = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'day')

    def __str__(self):
        return f"{self.user.username} - Day {self.day}: {self.amount}"

@receiver(post_save, sender=UserDailyReward)
def give_referrer_reward(sender, instance, created, **kwargs):
    if created and not instance.is_referral_reward:
        referral = Referral.objects.filter(referred=instance.user).first()
        if referral:
            referrer = referral.referrer
            reward_amount = Decimal(instance.amount) * Decimal('0.05')
            
            # Referrer için yeni bir UserDailyReward oluştur
            UserDailyReward.objects.create(
                user=referrer,
                day=instance.day,
                amount=reward_amount,
                is_referral_reward=True
            )
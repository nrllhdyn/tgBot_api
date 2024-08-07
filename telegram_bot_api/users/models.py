from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    telegram_user_id = models.CharField(max_length=50, unique=True)
    referral_link = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    by_referred = models.ForeignKey('self', on_null=True, blank=True, related_name='referrals')
    last_daily_reward = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.username
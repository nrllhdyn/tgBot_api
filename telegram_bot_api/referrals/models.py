from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals_given')
    referred = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals_received')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('referrer', 'referred')

    def __str__(self):
        return f"{self.referrer.username} referred {self.referred.username}"
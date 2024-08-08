from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrer')
    referred = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referrer.username} -> {self.referred.username}"
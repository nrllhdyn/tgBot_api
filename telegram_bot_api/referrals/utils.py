from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

def get_referral_link(user_id):
    return reverse('referral-list') + f'?referrer_id={user_id}'
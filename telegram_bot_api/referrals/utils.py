from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_referral_link(user_id, bot_username):
    return f"https://t.me/{bot_username}?start={user_id}"
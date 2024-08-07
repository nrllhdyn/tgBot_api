from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'telegram_user_id', 'referral_link', 'balance', 'status', 'by_referred', 'last_daily_reward']
        read_only_fields = ['id', 'referral_link', 'balance', 'status', 'last_daily_reward']

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'telegram_user_id', 'by_referred']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
from rest_framework import serializers
from .models import DailyReward, UserDailyReward

class DailyRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyReward
        fields = ['day', 'amount']

class UserDailyRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDailyReward
        fields = ['day', 'claimed_at', 'amount']
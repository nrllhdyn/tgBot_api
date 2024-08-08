from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import DailyReward, UserDailyReward
from .serializers import DailyRewardSerializer, UserDailyRewardSerializer
from referrals.models import Referral
from decimal import Decimal
from django.db import transaction

class DailyRewardViewSet(viewsets.ModelViewSet):
    queryset = DailyReward.objects.all()
    serializer_class = DailyRewardSerializer

class UserDailyRewardViewSet(viewsets.ModelViewSet):
    serializer_class = UserDailyRewardSerializer

    def get_queryset(self):
        return UserDailyReward.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def claim_reward(self, request):
        user = request.user
        today = timezone.now().date()

        if UserDailyReward.objects.filter(user=user, claimed_at__date=today, is_referral_bonus=False).exists():
            return Response({"detail": "You have already claimed your reward today."}, status=status.HTTP_400_BAD_REQUEST)

        last_claim = UserDailyReward.objects.filter(user=user, is_referral_bonus=False).order_by('-day').first()

        if last_claim:
            next_day = last_claim.day + 1
        else:
            next_day = 1

        if next_day > 12:
            next_day = 1  

        try:
            daily_reward = DailyReward.objects.get(day=next_day)
        except DailyReward.DoesNotExist:
            return Response({"detail": "Reward not found for this day."}, status=status.HTTP_404_NOT_FOUND)

        user_daily_reward = UserDailyReward.objects.create(
            user=user,
            day=next_day,
            amount=daily_reward.amount,
            is_referral_bonus=False
        )

        user.balance += daily_reward.amount
        user.save()

        serializer = self.get_serializer(user_daily_reward)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def reward_status(self, request):
        user = request.user
        claimed_rewards = UserDailyReward.objects.filter(user=user, is_referral_bonus=False).order_by('day')
        all_rewards = DailyReward.objects.all().order_by('day')

        status_list = []
        for reward in all_rewards:
            claimed = claimed_rewards.filter(day=reward.day).exists()
            status_list.append({
                "day": reward.day,
                "amount": reward.amount,
                "claimed": claimed
            })

        return Response(status_list)
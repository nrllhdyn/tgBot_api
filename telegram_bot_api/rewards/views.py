from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import DailyReward, UserDailyReward
from .serializers import DailyRewardSerializer, UserDailyRewardSerializer

class DailyRewardViewSet(viewsets.ModelViewSet):
    queryset = DailyReward.objects.all()
    serializer_class = DailyRewardSerializer

class UserDailyRewardViewSet(viewsets.ModelViewSet):
    serializer_class = UserDailyRewardSerializer

    def get_queryset(self):
        return UserDailyReward.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def claim_reward(self, request):
        user = request.user
        last_claim = UserDailyReward.objects.filter(user=user).order_by('-day').first()

        if last_claim:
            next_day = last_claim.day + 1
            if (timezone.now() - last_claim.claimed_at) < timedelta(days=1):
                return Response({"detail": "You can only claim one reward per day."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            next_day = 1

        if next_day > 12:
            next_day = 1  # Reset to day 1 after completing 12 days

        try:
            daily_reward = DailyReward.objects.get(day=next_day)
        except DailyReward.DoesNotExist:
            return Response({"detail": "Reward not found for this day."}, status=status.HTTP_404_NOT_FOUND)

        user_daily_reward = UserDailyReward.objects.create(
            user=user,
            day=next_day,
            amount=daily_reward.amount
        )

        user.balance += daily_reward.amount
        user.save()

        serializer = self.get_serializer(user_daily_reward)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def reward_status(self, request):
        user = request.user
        claimed_rewards = UserDailyReward.objects.filter(user=user).order_by('day')
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
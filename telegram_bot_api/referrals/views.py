from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Referral
from .serializers import ReferralSerializer
from .utils import generate_referral_link
from django.contrib.auth import get_user_model

User = get_user_model()

class ReferralViewSet(viewsets.ModelViewSet):
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer

    def create(self, request):
        referrer_id = request.data.get('referrer_id')
        referred_id = request.data.get('referred_id')

        if referrer_id and referred_id:
            try:
                referrer = User.objects.get(id=referrer_id)
                referred = User.objects.get(id=referred_id)
            except User.DoesNotExist:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            referral, created = Referral.objects.get_or_create(referrer=referrer, referred=referred)

            if created:
                return Response({'message': 'Referral created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Referral already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def my_referral_link(self, request):
        user = request.user
        bot_username = 'YOUR_BOT_USERNAME'  # Bot kullanıcı adınızı buraya ekleyin
        referral_link = generate_referral_link(user.id, bot_username)
        return Response({'referral_link': referral_link})

    @action(detail=False, methods=['get'])
    def my_referrals(self, request):
        user = request.user
        referrals = Referral.objects.filter(referrer=user)
        serializer = self.get_serializer(referrals, many=True)
        return Response(serializer.data)
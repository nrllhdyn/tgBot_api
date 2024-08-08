from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Referral
from .serializers import ReferralSerializer
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
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, UserCreateSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        referral_link = request.data.get('referral_link')
        if referral_link:
            try:
                referrer = User.objects.get(referral_link=referral_link)
                serializer.validated_data['by_referred'] = referrer
            except User.DoesNotExist:
                pass
        
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def start_bot(self, request, pk=None):
        user = self.get_object()
        # Bot başlatma işlemleri burada yapılacak
        return Response({'status': 'Bot started'})

    @action(detail=True, methods=['get'])
    def referrals(self, request, pk=None):
        user = self.get_object()
        referrals = user.referrals.all()
        serializer = UserSerializer(referrals, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_referral_link(self, request):
        user = request.user
        return Response({'referral_link': user.referral_link})
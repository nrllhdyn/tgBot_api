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
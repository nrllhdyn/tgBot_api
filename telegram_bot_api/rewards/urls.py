from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DailyRewardViewSet, UserDailyRewardViewSet

router = DefaultRouter()
router.register(r'daily-rewards', DailyRewardViewSet)
router.register(r'user-daily-rewards', UserDailyRewardViewSet, basename='user-daily-rewards')

urlpatterns = [
    path('', include(router.urls)),
]
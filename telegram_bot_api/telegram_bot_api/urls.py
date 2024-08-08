from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/rewards/', include('rewards.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/referrals/', include('referrals.urls')),
    path('api-token-auth/', obtain_auth_token),
]
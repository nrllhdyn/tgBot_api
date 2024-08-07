from django.contrib import admin
from .models import DailyReward

@admin.register(DailyReward)
class DailyRewardAdmin(admin.ModelAdmin):
    list_display = ('day', 'amount')
# from rest_framework import serializers
# from .models import Referral

# class ReferralSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Referral
#         fields = '__all__'

from rest_framework import serializers
from .models import Referral

class ReferralSerializer(serializers.ModelSerializer):
    referred_username = serializers.CharField(source='referred.username', read_only=True)

    class Meta:
        model = Referral
        fields = ['id', 'referrer', 'referred', 'referred_username', 'created_at']
from rest_framework import serializers
from .models import Plan, Subscription, ExchangeRateLog

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class ExchangeRateLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRateLog
        fields = '__all__'



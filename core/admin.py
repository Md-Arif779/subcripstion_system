from django.contrib import admin
from .models import Plan, Subscription, ExchangeRateLog

from django_celery_beat.models import PeriodicTask, IntervalSchedule


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'status')
    list_filter = ('status',)

@admin.register(ExchangeRateLog)
class ExchangeRateLogAdmin(admin.ModelAdmin):
    list_display = ('base_currency', 'target_currency', 'rate', 'fetched_at')
    list_filter = ('base_currency', 'target_currency')


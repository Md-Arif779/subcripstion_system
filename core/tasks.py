from celery import shared_task
import requests
from .models import ExchangeRateLog
from django.utils import timezone

@shared_task
def fetch_usd_to_bdt_exchange_rate():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()

    try:
        rate = data['rates']['BDT']
        ExchangeRateLog.objects.create(rate=rate, timestamp=timezone.now())
        return f"Saved rate: {rate}"
    except KeyError:
        return "BDT rate not found"

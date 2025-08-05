from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Subscription, Plan, ExchangeRateLog
from .forms import SubscriptionForm
from .serializers import SubscriptionSerializer

from datetime import timedelta
import requests


from django.contrib.auth.models import User
from rest_framework import generics, serializers
from rest_framework.permissions import AllowAny

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# === REST API Views ===

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe(request):
    try:
        plan_id = request.data.get("plan_id")
        plan = Plan.objects.get(id=plan_id)

        with transaction.atomic():
            start_date = timezone.now()
            end_date = start_date + timedelta(days=plan.duration_days)

            subscription = Subscription.objects.create(
                user=request.user,
                plan=plan,
                start_date=start_date,
                end_date=end_date,
                status='active'
            )

            serializer = SubscriptionSerializer(subscription)
            return Response(serializer.data, status=201)

    except Plan.DoesNotExist:
        return Response({"error": "Invalid plan ID"}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_subscriptions(request):
    subscriptions = Subscription.objects.filter(user=request.user)
    serializer = SubscriptionSerializer(subscriptions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_subscription(request):
    try:
        subscription_id = request.data.get("subscription_id")
        subscription = Subscription.objects.get(id=subscription_id, user=request.user)
        subscription.status = "cancelled"
        subscription.save()
        return Response({"message": "Subscription cancelled."})
    except Subscription.DoesNotExist:
        return Response({"error": "Subscription not found."}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exchange_rate_view(request):
    base = request.GET.get('base', 'USD')
    target = request.GET.get('target', 'BDT')

    url = f"https://v6.exchangerate-api.com/v6/d70cf87d650eb209a4d7bd19/pair/{base}/{target}"
    response = requests.get(url)
    data = response.json()

    if data.get('result') == 'success':
        rate = data['conversion_rate']

        ExchangeRateLog.objects.create(
            rate=rate,
            base_currency='USD',
            target_currency='BDT',
            fetched_at=timezone.now()
)


        return Response({
            'base': base,
            'target': target,
            'rate': rate,
            'time': data['time_last_update_utc']
        })
    else:
        return Response({'error': 'Failed to fetch exchange rate'}, status=400)



# === UI VIEWS ===

def home_view(request):
    subscriptions = Subscription.objects.all().select_related('plan', 'user')
    latest_rate = ExchangeRateLog.objects.order_by('-fetched_at').first()

    context = {
        'subscriptions': subscriptions,
        'latest_rate': latest_rate,
    }
    return render(request, 'home.html', context)



    
    context = {
        'subscriptions': subscriptions,
        'latest_rate': latest_rate,
    }
    return render(request, 'home.html', context)



@login_required
def create_subscription(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SubscriptionForm()
    return render(request, 'create_subscription.html', {'form': form})


@login_required
def edit_subscription(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SubscriptionForm(instance=subscription)
    return render(request, 'edit_subscription.html', {'form': form})


@login_required
def delete_subscription(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)
    if request.method == 'POST':
        subscription.delete()
        return redirect('home')
    return render(request, 'confirm_delete.html', {'subscription': subscription})


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Authenticated access successful!"})








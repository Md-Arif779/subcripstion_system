from django.urls import path
from .views import (
    subscribe, user_subscriptions, cancel_subscription, exchange_rate_view,
    home_view, create_subscription, edit_subscription, delete_subscription, ProtectedView, RegisterView
)

urlpatterns = [
    # UI views
    path('', home_view, name='home'),

    path('create/', create_subscription, name='create_subscription'),
    path('edit/<int:pk>/', edit_subscription, name='edit_subscription'),
    path('delete/<int:pk>/', delete_subscription, name='delete_subscription'),

    # API endpoints
    path('api/subscribe/', subscribe, name='subscribe'),
    path('api/subscriptions/', user_subscriptions, name='user_subscriptions'),
    path('api/cancel/', cancel_subscription, name='cancel_subscription'),
    path('api/exchange-rate/', exchange_rate_view, name='exchange_rate'),

    # Auth test
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('api/register/', RegisterView.as_view(), name='register'),
]






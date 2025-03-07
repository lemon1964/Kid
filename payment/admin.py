# backend/payment/admin.py
from django.contrib import admin
from .models import StripePayment, KassaPayment

@admin.register(StripePayment)
class StripePaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_type', 'amount', 'status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'status', 'stripe_payment_intent_id')
    list_filter = ('status', 'subscription_type')


@admin.register(KassaPayment)
class KassaPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_type', 'amount', 'status', 'kassa_payment_status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'status', 'kassa_payment_id', 'kassa_subscription_id')
    list_filter = ('status', 'subscription_type', 'kassa_payment_status')

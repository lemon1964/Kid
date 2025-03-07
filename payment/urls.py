from django.urls import path
from . import views, viewsStripe,  viewsKassa

app_name = 'payment'

urlpatterns = [
    # stripe
    path('process-buy/', viewsStripe.payment_process_buy, name='process_buy'),
    path('process-subscription/', viewsStripe.payment_process_subscription, name='process_subscription'),
    path('webhook/', viewsStripe.stripe_webhook, name='stripe-webhook'),
    # kassa
    # Первый платеж
    path('process-kassa/', viewsKassa.process_kassa, name='process_kassa'),
    # Вэбхуки от Кассы waiting_for_capture, succeeded, canceled, refund
    path('webhook-kassa/', viewsKassa.kassa_webhook, name='kassa_webhook'),
    # Подтверждение платежа
    path('confirm-payment/', viewsKassa.confirm_payment, name='confirm_payment'),
    # Повторный платеж Подписки по исходному первому платежу
    path('process-recurring-payment/', viewsKassa.process_recurring_payment, name='process_recurring_payment'),
    # Возврат платежа
    path('refund/', viewsKassa.process_refund, name='process_refund'),

    # common
    path('completed/', views.payment_completed, name='completed'),
    path('canceled/', views.payment_canceled, name='canceled'),
]

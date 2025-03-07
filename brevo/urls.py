from django.urls import path
from .views import payment_webhook, add_user_to_brevo, repeat_campaign, unsubscribe_webhook, webhook_test

urlpatterns = [
    path('webhook/', payment_webhook, name='send_email'),  # маршрут для вебхука от платежного сервиса
    path('adduser/', add_user_to_brevo, name='add_user_to_brevo'),  # маршрут для добавления пользователя в Brevo
    path('repeat_campaign/', repeat_campaign, name='repeat_campaign'),  # маршрут для повторения кампании
    path('unsubscribed-webhook/', unsubscribe_webhook, name='unsubscribe_webhook'),  # маршрут для вебхука от Brevo при отписке
    path('webhook-test/', webhook_test, name='webhook_test'),
]

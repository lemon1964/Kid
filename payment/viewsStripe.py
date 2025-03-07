from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.decorators import api_view
import stripe
from django.conf import settings
from django.urls import reverse
from .models import StripePayment

from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

import logging
logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

@api_view(['POST'])
def payment_process_buy(request):
    subscription_type = request.data.get('subscription_type')
    coupon_code = request.data.get('coupon_code')
    amount = 100

    if coupon_code:
        # Проводим валидацию промокода (можно добавить дополнительную логику для скидок)
        pass

    # Создание записи о платеже в базе данныхё
    payment = StripePayment.objects.create(
        user=request.user,
        amount=amount,
        subscription_type=subscription_type,
        coupon_code=coupon_code or '',
        discount=0,  # Можно вычислить, если есть промокод
        status='pending',  # Статус "pending", пока не подтверждено
        stripe_payment_intent_id=None,  # Сначала оставляем None
    )

    # Создание сессии Stripe с использованием ID нового платежа
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Kidbe Subscription',
                },
                'unit_amount': int(amount * 100),
            },
            'quantity': 1,
        }],
        mode='payment', # в режиме разовой покупки
        success_url=request.build_absolute_uri(reverse('payment:completed')),
        cancel_url=request.build_absolute_uri(reverse('payment:canceled')),
        client_reference_id=str(payment.id),  # Используем ID платежа для привязки
    )
    # Обновляем запись о платеже с stripe_payment_intent_id после создания сессии
    payment.stripe_payment_intent_id = session.payment_intent
    payment.save()

    return Response({
        'session_url': session.url,
        'payment_id': payment.id,
    })
    

@api_view(['POST'])
def payment_process_subscription(request):
    subscription_type = request.data.get('subscription_type')  # monthly, yearly, forever
    coupon_code = request.data.get('coupon_code', '')
    amount = 0  # Плата будет рассчитываться на основе выбранного продукта

    if coupon_code:
        # Проводим валидацию промокода (можно добавить дополнительную логику для скидок)
        pass

    # Создание записи о платеже в базе данных
    payment = StripePayment.objects.create(
        user=request.user,
        amount=amount,
        subscription_type=subscription_type,
        coupon_code=coupon_code or '',
        discount=0,  # Можно вычислить, если есть промокод
        status='pending',  # Статус "pending", пока не подтверждено
        stripe_subscription_id=None,  # здесь stripe_subscription_id
    )
    
    # Выбор продукта и цены на основе типа подписки
    if subscription_type == "monthly":
        price_id = "price_1QtakBP21hgowpHEnLpbsGmZ"  # ID для цены за месяц берем из Stripe
        amount = 3  # $3.00
    elif subscription_type == "yearly":
        price_id = "price_1QtalyP21hgowpHE3jqMBgQN"  # ID для цены за год берем из Stripe
        amount = 30  # $30.00
    else:
        return Response({"error": "Invalid subscription type"}, status=400)

    # Генерация URL сессии
    success_url = request.build_absolute_uri('/api/payment/completed/')
    cancel_url = request.build_absolute_uri('/api/payment/canceled/')

    # Создаем сессию для Stripe Checkout
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,  # Указываем ID для цены подписки
            'quantity': 1,
        }],
        mode='subscription',  # В режиме подписки
        success_url=success_url,
        cancel_url=cancel_url,
        client_reference_id=str(payment.id),  # ✅ payment.id
        # client_reference_id=str(request.user.id),  # Идентификатор пользователя для привязки
        metadata={'subscription_type': subscription_type, 'coupon_code': coupon_code}
    )
    
    # Обновляем запись о платеже с stripe_subscription_id после создания сессии
    payment.stripe_subscription_id = session.subscription  # Записываем ID подписки, если она есть
    payment.amount = amount
    payment.save()

    # Возвращаем URL сессии и ID платежа
    return Response({
        'session_url': session.url,
        'payment_id': session.id,  # Это ID сессии Stripe
    })
    


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f"Error constructing event: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Signature verification error: {e}")
        return HttpResponse(status=400)

    # Обработка различных типов событий Stripe
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        logger.info(f"Session completed: {session}")

        payment_intent = session.get('payment_intent', None)
        subscription_id = session.get('subscription', None)

        if payment_intent:
            try:
                # Разовая покупка
                payment = StripePayment.objects.get(id=session['client_reference_id'])
                payment.status = 'completed'
                payment.stripe_payment_intent_id = payment_intent  # Обновляем payment_intent
                if subscription_id:
                    payment.stripe_subscription_id = subscription_id  # Записываем subscription_id для подписки
                payment.save()

                # Применяем подписку для пользователя, если подписка
                user = payment.user
                user.is_subscribed_forever = True 
                user.save()

            except StripePayment.DoesNotExist:
                logger.error(f"Payment not found for intent {payment_intent}")
                return HttpResponse(status=404)

        elif subscription_id:
            try:
                # Подписка
                payment = StripePayment.objects.get(id=session['client_reference_id'])
                payment.status = 'completed'
                payment.stripe_subscription_id = subscription_id 
                # print("payment", payment)
                payment.save()

                # Применяем подписку для пользователя
                user = payment.user
                if payment.subscription_type == 'monthly':
                    user.is_subscribed_monthly = True
                elif payment.subscription_type == 'yearly':
                    user.is_subscribed_yearly = True
                user.save()

            except StripePayment.DoesNotExist:
                logger.error(f"Subscription not found for subscription {subscription_id}")
                return HttpResponse(status=404)

    return HttpResponse(status=200)


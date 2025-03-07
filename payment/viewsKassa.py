from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import uuid
from yookassa import Payment, Refund
from .models import KassaPayment
from .utils import create_receipt, create_payment_data, update_payment_status, confirm_payment_in_kassa, is_valid_webhook_signature
from .hooks import webhook_waiting_for_capture, webhook_succeeded, webhook_canceled, webhook_refund

from decouple import config
BASE_URL = config('BASE_URL')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_kassa(request):
    subscription_type = request.data.get('subscription_type')
    coupon_code = request.data.get('coupon_code')
    
    # Настройка значений для разового или подписного платежа
    if subscription_type == "monthly":
        amount = 300  # 3$ = 300 рублей
        description = "Ежемесячная подписка"
    elif subscription_type == "yearly":
        amount = 3000  # 30$ = 3000 рублей
        description = "Годовая подписка"
    elif subscription_type == "forever":
        amount = 10000  # Цена за разовую покупку
        description = "Оплата за покупку навсегда"
    else:
        return Response({"error": "Неизвестный тип подписки"}, status=400)
    
    # Достаем данные для чека
    receipt = create_receipt(request.user, description, amount)

    # Создание записи о платеже в базе данных
    payment = KassaPayment.objects.create(
        user=request.user,
        amount=amount,
        subscription_type=subscription_type,
        coupon_code=coupon_code or '',
        discount=0,  # Можете добавить логику для скидок
        status='pending',
    )

    # Создание данных для платежа в Кассе
    payment_data = create_payment_data(amount, description, payment.id, subscription_type, receipt)
 
    idempotence_key = str(uuid.uuid4())

    try:
        # Создание платежа в Кассе
        kassa_payment = Payment.create(payment_data, idempotence_key)

        # Сохраняем kassa_payment_id в базе
        payment.kassa_payment_id = kassa_payment.id
        payment.save()

        # Возвращаем ссылку для подтверждения платежа
        return Response({
            'session_url': kassa_payment.confirmation.confirmation_url
        }, status=200)
    except Exception as e:
        print(f"Ошибка при создании платежа: {e}")
        # Удаляем созданный платеж из базы, если произошла ошибка при запросе в Кассу
        payment.delete()  # Удаляем платеж из базы
        return Response({'error': 'Ошибка при создании платежа'}, status=500)
    
    
# Основной обработчик webhook
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def kassa_webhook(request):
    # Проверка корректность подписи уведомления
    if not is_valid_webhook_signature(request):
        return Response({'error': 'Invalid untrusted IP address'}, status=400)
        
    data = request.data  # Получаем данные уведомления от ЮKассы
    event_type = data.get('event', '')
    
    # Направляем в соответствующую функцию в зависимости от типа события
    if event_type == 'payment.waiting_for_capture':
        return webhook_waiting_for_capture(data)
    elif event_type == 'payment.succeeded':
        return webhook_succeeded(data)
    elif event_type == 'payment.canceled':
        return webhook_canceled(data)
    elif event_type == 'refund.succeeded':
        return webhook_refund(data)
    
    # Если событие не найдено, возвращаем ошибку
    return Response({'error': 'Invalid event'}, status=400)



@api_view(['POST'])
@permission_classes([AllowAny])
def confirm_payment(request):
    payment_id = request.data.get('payment_id')
    amount = request.data.get('amount')

    if not payment_id or not amount:
        return Response({"error": "payment_id and amount are required"}, status=400)

    # Подтверждаем платеж в ЮKассе с правильной суммой
    kassa_response = confirm_payment_in_kassa(payment_id, amount)

    if kassa_response:
        # Обновляем запись в базе данных, используя данные из ответа Кассы
        if update_payment_status(payment_id, kassa_response):
            return Response({"status": "Payment confirmed"}, status=200)
        else:
            return Response({"error": "Payment not found or failed to update status"}, status=404)
    else:
        return Response({"error": "Error confirming payment in Kassa"}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def process_recurring_payment(request):
    # Получаем payment_method_id из запроса
    payment_method_id = request.data.get('payment_method_id')
    
    if not payment_method_id:
        return Response({'error': 'payment_method_id is required'}, status=400)
    
    # Ищем исходный платеж в базе данных по kassa_payment_id (payment_method_id)
    try:
        original_payment = KassaPayment.objects.get(kassa_payment_id=payment_method_id)
    except KassaPayment.DoesNotExist:
        return Response({'error': 'Original payment not found'}, status=404)
    
    # Достаем данные для чека из оригинального платежа
    receipt = create_receipt(original_payment.user, original_payment.subscription_type, original_payment.amount)
    
    # Создаем новый платеж, копируя только нужные поля (исключаем поле 'id')
    payment_data = {
        'amount': original_payment.amount,
        'subscription_type': original_payment.subscription_type,
        'coupon_code': original_payment.coupon_code,
        'discount': original_payment.discount,
        'status': 'pending',  # Статус платежа пока "pending"
        'created_at': timezone.now(),  # Устанавливаем новую дату
        'updated_at': timezone.now(),
        'user': original_payment.user,
        'information_payment': "Повторный",  # Уникальный идентификатор для повторного платежа
        'kassa_payment_status': "waiting_for_capture",  # Статус платежа в Кассе
        'income_amount': original_payment.income_amount,  # Сумма после комиссии
    }

    # Создаем новый экземпляр платежа на основе данных старого
    payment = KassaPayment.objects.create(**payment_data)
    
    # Параметры для нового платежа
    payment_data = create_payment_data(payment.amount, payment.subscription_type, payment.id, payment.subscription_type, receipt, payment_method_id)

    # Генерируем уникальный idempotence_key
    idempotence_key = str(uuid.uuid4())

    try:
        # Создаем новый платеж, используя сохраненный метод оплаты
        new_payment = Payment.create(payment_data, idempotence_key)
        
        # Обновляем созданный платеж в базе
        payment.kassa_payment_id = new_payment.id  # Обновляем kassa_payment_id на новый ID

        # Сохраняем все обновления в базе
        payment.save()
        # Платеж обновится в базе и в Кассе по хуку payment.succeeded
        # Без хука его можно обновить вручную через POST запрос на /api/payment/confirm-payment/
        
        return Response({
            'payment_id': new_payment.id
        }, status=200)
    except Exception as e:
        # Удаляем созданный платеж из базы, если произошла ошибка при запросе в Кассу
        payment.delete()  # Удаляем платеж из базы
        return Response({'error': f'Error creating recurring payment: {str(e)}'}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def process_refund(request):
    # Получаем необходимые данные из запроса
    payment_id = request.data.get('payment_id')
    amount = request.data.get('amount')
    description = request.data.get('description', '')  # Комментарий к возврату
    receipt = request.data.get('receipt')  # Данные для чека (необязательные)

    if not payment_id or not amount:
        return Response({'error': 'payment_id and amount are required'}, status=400)
    
    # Достаем пользователя, связанного с этим платежом
    try:
        payment = KassaPayment.objects.get(kassa_payment_id=payment_id)
    except KassaPayment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=404)

    # Достаем данные для чека, если не переданы
    if not receipt:
        receipt = create_receipt(payment.user, payment.subscription_type, amount)

    # Параметры для возврата
    refund_data = {
        "amount": {
            "value": str(amount),  # Сумма возврата
            "currency": "RUB"
        },
        "payment_id": payment_id,
        "description": description,
        "receipt": receipt
    }

    try:
        # Создаем возврат
        refund = Refund.create(refund_data)
        
        # Отладка: смотрим структуру объекта refund
        # print("Refund object:", refund)

        # Преобразуем объект в словарь
        if hasattr(refund, '__dict__'):
            refund_data = vars(refund)
        else:
            refund_data = refund  # если это уже словарь, работаем с ним напрямую
        
        # Печатаем все поля объекта, чтобы увидеть его структуру
        # print("Refund data dictionary:", refund_data)
        
        # Извлекаем информацию о возврате (authorization details)
        refund_authorization_details = refund_data.get('refund_authorization_details', None)
        
        # Записываем авторизационные детали, если они существуют
        if refund_authorization_details:
            payment.authorization_details = refund_authorization_details
            print("Updated payment.authorization_details:", payment.authorization_details)
        else:
            print("No refund authorization details found.")
        
        # Сохраняем изменения в базе данных
        payment.save()

        # Возвращаем успешный ответ с id возврата
        return Response({
            'refund_id': refund.id,
            'status': refund.status,
            'amount': refund.amount,
        }, status=200)
    
    except Exception as e:
        print(f"Error processing refund: {e}")
        return Response({'error': 'Error processing refund'}, status=500)


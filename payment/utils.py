from decimal import Decimal
from datetime import datetime
from django.utils.timezone import make_aware
import uuid
from yookassa import Payment
import ipaddress
from .models import KassaPayment
from decouple import config

BASE_URL = config('BASE_URL')

def create_receipt(user, description, amount):
    """
    Функция для создания данных чека для Кассы.
    """
    return {
        "customer": {
            "full_name": user.name,
            "email": user.email,
        },
        "items": [
            {
                "description": description,
                "quantity": "1.00",
                "amount": {
                    "value": str(amount),
                    "currency": "RUB"
                },
                "vat_code": "2",  # Пример кода НДС
                "payment_mode": "full_payment",
                "payment_subject": "commodity",
                "country_of_origin_code": "RU",
                "product_code": "Кидби приложение",
                "excise": "0.00",  # Пример акциза
                "supplier": {
                    "name": "Кидби",
                    "phone": "123456789",
                    "inn": "123106123985"
                }
            },
        ]
    }


def create_payment_data(amount, description, payment_id, subscription_type, receipt, payment_method_id=None):
    """
    Функция для создания данных для платежа в Кассе.
    Пять параметров для первого платежа, шестой payment_method_id нужен для повторных платежей по Подписке.
    """
    payment_data = {
        'amount': {
            'value': str(amount),
            'currency': 'RUB'
        },
        'confirmation': {
            'type': 'redirect',
            'return_url': f"{BASE_URL}/api/payment/completed/"
        },
        'description': description,
        'metadata': {
            'payment_id': payment_id,
            'subscription_type': subscription_type
        },
        'receipt': receipt,  # Добавляем данные чека
    }

    if payment_method_id:
        payment_data['payment_method_id'] = payment_method_id  # Если передан payment_method_id, добавляем его в данные

    return payment_data

def update_payment_status(payment_id, kassa_response):
    """
    Функция для обновления статуса платежа в базе данных после подтверждения в Кассе.
    """
    try:
        # Преобразуем объект в словарь, если это необходимо
        if hasattr(kassa_response, '__dict__'):
            kassa_data = vars(kassa_response)
        else:
            kassa_data = kassa_response  # если уже словарь, работаем с ним напрямую

        # Ищем платеж в базе данных по kassa_payment_id
        kassa_payment = KassaPayment.objects.get(kassa_payment_id=payment_id)

        # Обновляем статус на "succeeded"
        kassa_payment.kassa_payment_status = 'succeeded'
        kassa_payment.status = 'completed'  # Статус платежа меняем на "completed"

        # Применяем комиссию, если требуется
        kassa_payment.income_amount = kassa_payment.amount - Decimal('0.03') * kassa_payment.amount  # Пример вычисления комиссии

        # Записываем способ платежа
        payment_method = kassa_data.get('_PaymentResponse__payment_method', None)
        if payment_method:
            # Доступ к атрибутам объекта PaymentDataBankCard
            kassa_payment.payment_method = {
                "type": payment_method.type,
                "id": payment_method.id,
                "status": payment_method.status,
                "title": payment_method.title,
                "card": {
                    "first6": payment_method.card.first6,
                    "last4": payment_method.card.last4,
                    "expiry_year": payment_method.card.expiry_year,
                    "expiry_month": payment_method.card.expiry_month,
                    "card_type": payment_method.card.card_type,
                    "issuer_country": payment_method.card.issuer_country
                }
            }

        # Заполняем поле expires_at, если оно присутствует в данных
        card_info = kassa_payment.payment_method.get('card', {})
        if card_info:
            expiry_year = card_info.get('expiry_year')
            expiry_month = card_info.get('expiry_month')
            if expiry_year and expiry_month:
                try:
                    # Формируем строку вида "YYYY-MM-01" и преобразуем в datetime
                    expires_str = f"{expiry_year}-{expiry_month}-01"  # Устанавливаем 1-е число месяца
                    expires_naive = datetime.fromisoformat(expires_str)

                    # Преобразуем наивную дату в aware (с учетом часового пояса)
                    kassa_payment.expires_at = make_aware(expires_naive)
                except ValueError:
                    print(f"Ошибка преобразования даты: {expires_str}")

        # Заполняем поле authorization_details
        authorization_details = kassa_data.get('_PaymentResponse__authorization_details')
        if authorization_details:
            kassa_payment.authorization_details = {
                "rrn": authorization_details.rrn,
                "auth_code": authorization_details.auth_code,
                "three_d_secure": {
                    "applied": authorization_details.three_d_secure.applied,
                    "method_completed": authorization_details.three_d_secure.method_completed,
                    "challenge_completed": authorization_details.three_d_secure.challenge_completed
                }
            }

        # Обновляем другие поля, если нужно
        kassa_payment.save()

        # Лишний блок, можно убрать, user уже привязан к платежу
        # # Обновляем информацию о подписке для пользователя
        # user = kassa_payment.user
        # if kassa_payment.subscription_type == 'monthly':
        #     user.is_subscribed_monthly = True
        # elif kassa_payment.subscription_type == 'yearly':
        #     user.is_subscribed_yearly = True
        # elif kassa_payment.subscription_type == 'forever':
        #     user.is_subscribed_forever = True
        # user.save()

        # Логируем успешное подтверждение
        print(f"Платеж {kassa_payment.id} подтвержден и статус обновлен на 'succeeded'.")
        return True

    except KassaPayment.DoesNotExist:
        print(f"Платеж с ID {payment_id} не найден.")
        return False


def confirm_payment_in_kassa(payment_id, amount):
    """
    Функция для подтверждения платежа в ЮКассе.
    """
    try:
        # Генерируем уникальный idempotence_key для запроса
        idempotence_key = str(uuid.uuid4())

        # Подтверждаем платеж в ЮKассе с правильной суммой
        response = Payment.capture(payment_id, {
            "amount": {
                "value": str(amount),  # Используем извлеченную сумму
                "currency": "RUB"
            }
        }, idempotence_key)

        # Возвращаем ответ Кассы для дальнейшего использования
        return response
    except Exception as e:
        print(f"Error confirming payment in Kassa: {e}")
        return None
    

# Проверка корректности подписи уведомления в хуках от Кассы
def is_valid_webhook_signature(request):
    # Список доверенных IP-адресов
    ALLOWED_IP_RANGES = [
        '185.71.76.0/27',
        '185.71.77.0/27',
        '77.75.153.0/25',
        '77.75.156.11',
        '77.75.156.35',
        '77.75.154.128/25',
        '2a02:5180::/32',
    ]
    # Проверка IP-адреса
    ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0] or request.META.get('REMOTE_ADDR')
    is_ip_valid = any(ipaddress.ip_address(ip) in ipaddress.IPv4Network(range) for range in ALLOWED_IP_RANGES)

    if not is_ip_valid:
        print("Invalid untrusted IP address.")
        return False

    return True

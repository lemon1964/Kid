import requests
from rest_framework.response import Response
from datetime import datetime
from django.utils.timezone import make_aware
from .models import KassaPayment
from .utils import confirm_payment_in_kassa

from decouple import config
BASE_URL = config('BASE_URL')

def webhook_waiting_for_capture(data):
    payment_id = data.get('object', {}).get('id')
    amount = data.get('object', {}).get('amount', {}).get('value', 0)

    # Подтверждаем платеж в ЮKассе с правильной суммой
    if confirm_payment_in_kassa(payment_id, amount):
        return Response(status=200)
    else:
        return Response({"error": "Error confirming payment"}, status=500)


def webhook_succeeded(data):
    payment_id = data.get('object', {}).get('id')
    amount = data.get('object', {}).get('amount', {}).get('value', 0)

    # Отправляем запрос на подтверждение платежа в нашу систему
    confirm_url = f"{BASE_URL}/api/payment/confirm-payment/"  # URL для confirm_payment
    response = requests.post(confirm_url, json={'payment_id': payment_id, 'amount': amount})

    if response.status_code == 200:
        return Response(status=200)
    else:
        return Response({"error": "Error confirming payment"}, status=500)


def webhook_canceled(data):
    payment_id = data.get('object', {}).get('id')

    if payment_id:
        try:
            # Ищем платеж в базе данных по kassa_payment_id
            kassa_payment = KassaPayment.objects.get(kassa_payment_id=payment_id)

            # Обновляем статус платежа на "Canceled"
            kassa_payment.kassa_payment_status = 'canceled'
            kassa_payment.status = 'failed'  # Платеж не завершился, поэтому статус "failed"
            
            # Записываем причину отмены в information_payment
            cancellation_reason = data.get('object', {}).get('cancellation_details', {}).get('reason', 'Unknown')
            kassa_payment.information_payment = cancellation_reason  # Причина отмены

            # Заполняем поле expires_at, если оно присутствует в данных
            card_info = data.get('object', {}).get('payment_method', {}).get('card', {})
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

            # Заполняем поле payment_method
            payment_method = data.get('object', {}).get('payment_method', {})
            if payment_method:
                kassa_payment.payment_method = payment_method  # Сохраняем метод оплаты

            # Заполняем поле authorization_details
            authorization_details = data.get('object', {}).get('authorization_details', {})
            if authorization_details:
                kassa_payment.authorization_details = authorization_details  # Сохраняем детали авторизации

            # Сохраняем все изменения в базе
            kassa_payment.save()

            # Логируем успешное обновление
            print(f"Платеж {kassa_payment.id} отменен. Статус обновлен на 'canceled'. Причина отмены: {cancellation_reason}")
            return Response(status=200)

        except KassaPayment.DoesNotExist:
            print(f"Платеж с ID {payment_id} не найден.")
            return Response({'error': 'Платеж не найден'}, status=404)
        except Exception as e:
            print(f"Ошибка при обработке отмены: {e}")
            return Response({'error': 'Ошибка при обработке отмены'}, status=500)

    return Response({'error': 'payment_id is missing'}, status=400)


# Обработка события refund.succeeded (заглушка)
def webhook_refund(data):
    # print(f"Получен webhook с событием refund.succeeded: {json.dumps(data, indent=4)}")

    payment_id = data.get('object', {}).get('payment_id')
    refund_status = data.get('object', {}).get('status')
    cancellation_details = data.get('cancellation_details', {})
    description = data.get('object', {}).get('description', '')
    
    if payment_id:
        try:
            kassa_payment = KassaPayment.objects.get(kassa_payment_id=payment_id)
            
            # Записываем информацию о возврате
            if refund_status == 'succeeded':    # Успешний возврат
                kassa_payment.kassa_payment_status = 'refund_succeeded'
                kassa_payment.status = 'refund'
                kassa_payment.information_payment = description  # Описание возврата
            else:   # Не успешный возврат
                # kassa_payment.kassa_payment_status = 'succeeded'  // Оставляем прежний статус и вообще убираем строку
                kassa_payment.status = 'refund_failed'  # Для неудачного возврата статус 'failed'
                kassa_payment.information_payment = cancellation_details.get('reason', 'Unknown reason')  # Причина неуспешного возврата
            
            # Сохраняем данные возврата в базу
            kassa_payment.save()
            
            return Response(status=200)
        except KassaPayment.DoesNotExist:
            print(f"Платеж с ID {payment_id} не найден.")
            return Response({'error': 'Payment not found'}, status=404)
    return Response(status=200)


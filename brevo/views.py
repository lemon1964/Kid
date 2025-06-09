import os
from dotenv import load_dotenv
from django.core.mail import send_mail
from rest_framework.response import Response
from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi
from sib_api_v3_sdk.models import SendSmtpEmail

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sib_api_v3_sdk import ContactsApi, CreateContact, AddContactToList
from sib_api_v3_sdk.rest import ApiException
import json

from sib_api_v3_sdk import EmailCampaignsApi
# from sib_api_v3_sdk.models import UpdateEmailCampaign

from sib_api_v3_sdk.models.create_email_campaign import CreateEmailCampaign
from sib_api_v3_sdk.models.create_email_campaign_recipients import CreateEmailCampaignRecipients

from django.contrib.auth import get_user_model
User = get_user_model()

# Загрузка переменных окружения из .env
load_dotenv()

BREVO_API_KEY = os.getenv('BREVO_API_KEY')


@api_view(['POST'])
@permission_classes([AllowAny])  # Разрешает доступ всем запросам
@csrf_exempt  # Отключаем CSRF защиту для вебхуков
def payment_webhook(request):
    """
    Обрабатывает запросы вебхука и отправляет письма пользователю.
    """
    data = request.data
    user_email = data.get('email')
    if not user_email:
        return Response({"error": "Email is required"}, status=400)

    errors = []

    # Попытка отправки письма через SMTP
    smtp_response = send_email_via_server(user_email)
    if smtp_response.get("error"):
        errors.append(smtp_response["error"])

    # Попытка отправки письма через Brevo
    template_id = 1  # передаем шаблон для вебхука
    brevo_response = send_email_via_brevo(user_email, template_id)
    if brevo_response.get("error"):
        errors.append(brevo_response["error"])

    # Итоговый ответ
    if errors:
        return Response({"message": "Some errors occurred", "errors": errors}, status=500)
    return Response({"message": "Emails sent successfully"}, status=200)

def send_email_via_server(email):
    """
    Отправляет письмо пользователю через SMTP.
    """
    try:
        send_mail(
            subject='Успешная оплата SMTP',
            message='Спасибо за вашу подписку! SMTP на связи.',
            from_email='sv444444@gmail.com',
            recipient_list=[email],
            fail_silently=False,
        )
        return {"message": "SMTP email sent successfully"}
    except Exception as e:
        return {"error": str(e)}


def send_email_via_brevo(email, template_id=None):
    """
    Отправляет письмо пользователю через Brevo API с использованием шаблона.
    """
    config = Configuration()
    config.api_key['api-key'] = BREVO_API_KEY  # Берем ключ из переменной окружения
    api_client = ApiClient(configuration=config)
    email_api = TransactionalEmailsApi(api_client)

    # # ID шаблона, который мы будем использовать
    # template_id = 1  # Замените на ваш актуальный ID шаблона

    send_smtp_email = SendSmtpEmail(
        to=[{"email": email}],
        template_id=template_id,  # Указываем ID шаблона
        sender={"email": "sv444444@gmail.com", "name": "KidBe"},  # Подтвержденный email
        reply_to={"email": "lemon.design@mail.ru"}  # Email для ответов
    )

    try:
        email_api.send_transac_email(send_smtp_email)
        print("Brevo email sent successfully")
        return {"message": "Brevo email sent successfully"}
    except Exception as e:
        return {"error": str(e)}
    

@csrf_exempt
@permission_classes([AllowAny])
def add_user_to_brevo(request):
    if request.method == "POST":
        try:
            # Получение email из запроса
            data = json.loads(request.body)
            email = data.get("email", "").strip()

            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)

            # Настраиваем API Brevo
            config = Configuration()
            config.api_key['api-key'] = BREVO_API_KEY
            api_client = ApiClient(configuration=config)
            contacts_api = ContactsApi(api_client)

            # Добавление/обновление контакта
            contact = CreateContact(email=email)
            try:
                contacts_api.create_contact(contact)
                print(f"Contact {email} added successfully.")
            except ApiException as e:
                error_response = str(e)
                if "duplicate_parameter" in error_response:
                    print(f"Contact {email} already exists. Attempting to update...")
                    # Добавляем обновление контакта
                    try:
                        contacts_api.update_contact(email, contact)
                        print(f"Contact {email} updated successfully.")
                        return {"message": "Brevo email sent successfully (updated contact)."}
                    except ApiException as update_error:
                        return {"error": f"Failed to update contact: {str(update_error)}"}
                else:
                    return {"error": f"Failed to add/update contact: {error_response}"}

            # Добавление контакта в список с ID 2
            LIST_ID = 2
            try:
                contacts_api.add_contact_to_list(
                    list_id=LIST_ID,
                    contact_emails={"emails": [email]}
                )
                print(f"Contact {email} added to list ID {LIST_ID}.")
            except ApiException as e:
                return JsonResponse({"error": f"Failed to add contact to list: {str(e)}"}, status=500)

            return JsonResponse({"message": f"Contact {email} successfully added/updated in Brevo and added to list ID {LIST_ID}."}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt  # Отключаем CSRF защиту для вебхуков
def repeat_campaign(request):
    campaign_id = request.data.get("campaign_id")

    if not campaign_id:
        return Response({"error": "campaign_id is required"}, status=400)

    try:
        # Настройка API Brevo
        config = Configuration()
        config.api_key['api-key'] = BREVO_API_KEY
        api_client = ApiClient(configuration=config)
        email_campaigns_api = EmailCampaignsApi(api_client)

        # Получение данных оригинальной кампании
        campaign = email_campaigns_api.get_email_campaign(int(campaign_id))
        print(f"Original campaign sender: {campaign.sender}")

        # Указание получателей через listIds
        recipients = CreateEmailCampaignRecipients(list_ids=[2,])

        # Создание новой кампании
        new_campaign_data = CreateEmailCampaign(
            name=f"{campaign.name} (Repeated)",  # Новое имя кампании
            subject=campaign.subject,
            sender={"email": "lemon.design@mail.ru", "name": "Kidbe"},
            html_content=campaign.html_content,
            recipients=recipients  # Передаем объект `recipients`
        )
        new_campaign = email_campaigns_api.create_email_campaign(new_campaign_data)
        print(f"New campaign created with ID: {new_campaign.id}")

        # Отправка новой кампании
        email_campaigns_api.send_email_campaign_now(new_campaign.id)
        print(f"Campaign {new_campaign.id} sent successfully!")

        return Response({"success": f"Campaign {new_campaign.id} repeated and sent successfully!"})

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt  # Отключаем CSRF защиту для вебхуков
def unsubscribe_webhook(request):
    if request.method == "POST":
        try:
            # Парсим данные из вебхука
            payload = json.loads(request.body)
            event = payload.get("event")
            email = payload.get("email")
            print("Webhook received:", payload)

            # Если событие 'unsubscribe' и email существует
            if event == "unsubscribe" and email:
                # Ищем пользователя по email
                user = User.objects.filter(email=email).first()

                if user:
                    # Обновляем статус подписки на False
                    user.newsletter = False
                    user.save()

                    return JsonResponse({"message": "User successfully unsubscribed"}, status=200)
                else:
                    return JsonResponse({"error": "User not found"}, status=404)
            else:
                return JsonResponse({"error": "Invalid event or missing email"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid HTTP method"}, status=405)




@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt  # Отключаем CSRF защиту для тестирования
def webhook_test(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body)
            print("Webhook received:", payload)
            return JsonResponse({"message": "Webhook received successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid HTTP method"}, status=405)


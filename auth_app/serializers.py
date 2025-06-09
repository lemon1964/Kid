from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import PasswordResetSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from allauth.account.utils import send_email_confirmation


from backend import settings
from brevo.views import send_email_via_brevo
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
import time

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['name'] = user.name
        token['provider'] = user.provider  # Добавлено
        return token

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }
        return super().validate(credentials)
    

class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(required=True)
    provider = serializers.CharField(required=False, default='credentials')

    def save(self, request):
        user = super().save(request)
        user.name = self.validated_data['name']
        user.provider = self.validated_data.get('provider', 'credentials')
        user.is_active = False  # Устанавливаем пользователя неактивным до подтверждения
        user.save()

        # Генерация ссылки подтверждения
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        # domain = settings.DOMAIN # Укажите свой порт
        # domain = "localhost:8000"  # Укажите свой порт
        confirmation_url = f"http://{settings.DOMAIN}{reverse('custom_verify_email')}?uid={uid}&token={token}"
        # confirmation_url = f"http://{domain}{reverse('custom_verify_email')}?uid={uid}&token={token}"
        # domain = get_current_site(request).domain
        # confirmation_url = f"http://{domain}{reverse('custom_verify_email')}?uid={uid}&token={token}"
                   
        # Отправка письма через Django SMTP
       # Отправка письма через Django SMTP с HTML-содержимым
        subject = "Email Confirmation"
        message = f"Please confirm your email using the following link: {confirmation_url}"
        html_message = f"""
        <html>
            <body>
                <p>Please confirm your email using the following link:</p>
                <p><a href="{confirmation_url}">Click here to confirm your email</a></p>
            </body>
        </html>
        """
        send_mail(
            subject,
            message,
            from_email={settings.EMAIL_HOST_USER},  # Укажите свой адрес отправителя EMAIL_HOST_USER
            recipient_list=[user.email],
            html_message=html_message  # Передаем HTML-сообщение для кликабельной ссылки
        )
        # send_mail(
        #     subject="Email Confirmation",
        #     message=f"Please confirm your email using the following link: {confirmation_url}",
        #     from_email="sv444444@gmail.com",
        #     recipient_list=[user.email],
        # )

        # Отправка письма "Please confirm your email" через Brevo
        # time.sleep(5)  # Задержка отправки, чтобы Brevo успел зарегистрировать пользователя
        # send_email_via_brevo(user.email, template_id=15)

        return user


class OAuthUserSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)
    provider = serializers.CharField(required=True)

    def validate_provider(self, value):
        allowed_providers = ['google', 'facebook', 'github']  # Разрешенные провайдеры
        if value not in allowed_providers:
            raise serializers.ValidationError(f"Provider {value} is not supported.")
        return value
    

class CustomPasswordResetSerializer(PasswordResetSerializer):
    def get_email_options(self):
        request = self.context.get('request')
        uid = self.context.get('uid', '')  # Теперь uid должен быть в контексте
        token = self.context.get('token', '')  # Аналогично
        reset_url = f"{settings.FRONT_URL}/auth/password-reset/{uid}/{token}/"
                
        return {
            "subject": "Password Reset",
            "extra_email_context": {"reset_url": reset_url},
        }


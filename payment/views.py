from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import HttpResponseRedirect
from backend import settings

@api_view(['GET'])
@permission_classes([AllowAny])
def payment_completed(request):
    # После успешной оплаты, формируем URL для фронтенда (например, главная страница или страница профиля)
    frontend_url = f"{settings.FRONT_URL}/payment/success"  # Здесь можно указать нужный путь на фронте
    # frontend_url = f"http://localhost:3000/payment/success"  # Здесь можно указать нужный путь на фронте
    return HttpResponseRedirect(frontend_url)

@api_view(['GET'])
@permission_classes([AllowAny])  # Разрешает доступ всем запросам
def payment_canceled(request):
    # После отмены оплаты, формируем URL для фронтенда (например, страница с повторной попыткой)
    frontend_url = f"{settings.FRONT_URL}/payment/canceled"  # Путь на фронт для отмены
    return HttpResponseRedirect(frontend_url)


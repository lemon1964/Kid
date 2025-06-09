from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/auth/', include('auth_app.urls')),  # Все пути auth перенесены в auth_app.urls
    path('accounts/', include('allauth.urls')),  # Пути для верификации email    
    path('api/brevo/', include('brevo.urls')),  # Namespace для brevo
    path('api/quiz/', include('quiz_app.urls')),  # Подключаем quiz_app
    path("api/dragdrop/", include("dragdrop_app.urls")),  # Подключаем Drag & Drop
    path("api/pixi/", include("pixi_app2.urls")),  # Подключаем Pixi
    path("api/task/", include("common.urls")),  # Универсальный API `common`
    path("api/payment/", include("payment.urls")),  # API для платежного сервиса
    path('', lambda request: HttpResponse("Welcome to Django Auth Module!")),
]

# Добавляем только в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# cd backend
# python manage.py runserver
# cd frontend
# npm run dev

# python manage.py makemigrations
# python manage.py migrate

# python manage.py createsuperuser
# lemon@lemon.com
# 12345


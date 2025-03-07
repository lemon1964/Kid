from pathlib import Path
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("DJANGO_SECRET_KEY")

# Определение окружения (local или production)
DJANGO_ENV = config('DJANGO_ENV')

if DJANGO_ENV == 'local':
    # Локальная база данных (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    
    DEBUG = config('DEBUG', default=True, cast=bool)
    CSRF_COOKIE_SECURE = False
    CSRF_COOKIE_HTTPONLY = False
    
    # ALLOWED_HOSTS = ['*']
    ALLOWED_HOSTS = [
    '127.0.0.1',  # Локальный хост для тестов
    'localhost',  # Чтобы поддерживать локальный доступ через localhost
    '24ce-46-101-80-16.ngrok-free.app',  # Ваш ngrok URL для публичных запросов
]
    CORS_ALLOW_ALL_ORIGINS = True
    
else:
    # База данных для продакшена (MySQL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT', cast=int),
        }
    }
    
    DEBUG = False
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True

    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())
    CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='', cast=Csv())


# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config("DEBUG", default=True, cast=bool)

# ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=lambda v: v.split(","))
# ALLOWED_HOSTS = [
#     '127.0.0.1',  # Локальный хост для тестов
#     'localhost',  # Чтобы поддерживать локальный доступ через localhost
#     '24ce-46-101-80-16.ngrok-free.app',  # Ваш ngrok URL для публичных запросов
# ]

INSTALLED_APPS = [
    'django.contrib.sites',  # Обязательно для django-allauth
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'corsheaders',
    'auth_app',
    'brevo',
    'quiz_app',
    'dragdrop_app',
    'pixi_app2',
    "common",
    'payment',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'corsheaders.middleware.CorsMiddleware',  # Должен быть добавлен перед 'CommonMiddleware'
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'allauth.account.middleware.AccountMiddleware',  # Добавляем сюда

]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✅ Разрешаем отдачу `.svg` (если есть ограничения)
# import mimetypes
# mimetypes.add_type("image/svg+xml", ".svg", True)


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
          
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


AUTH_USER_MODEL = 'auth_app.User'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Настройка почтового сервера Для Gmail
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

# Настройки аутентификации через email
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True  # Требуем email при регистрации
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Требуем верификацию email
ACCOUNT_AUTHENTICATED_REDIRECT_URL = "/"  # Переадресация после успешной аутентификации

# Настройка для dj_rest_auth
REST_USE_JWT = True  # Используем JWT для аутентификации

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}


SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # По умолчанию
    'allauth.account.auth_backends.AuthenticationBackend',  # allauth
]

# разрешаем временно для приема вэбхука от stripe
# CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",  # Ваш фронтенд
#     "http://127.0.0.1:3000",
# ]
# разрешить запросы с любого домена

CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-csrftoken",
    "x-requested-with",
    'Cache-Control',
]

REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "backend.auth_app.serializers.CustomRegisterSerializer",
    # В случае, если вы хотите использовать отдельный сериализатор для OAuth регистрации,
    # добавьте его сюда. Например, если у вас есть сериализатор для соцсетей:
    "OAUTH_REGISTER_SERIALIZER": "backend.auth_app.serializers.OAuthUserSerializer",
    "VERIFY_EMAIL": "path.to.CustomVerifyEmailView",
}

DJANGO_SETTINGS_MODULE = {
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}/',
}

# # для работы с ngrok
# CSRF_COOKIE_SECURE = False  # Для тестирования на локальном сервере
# CSRF_COOKIE_HTTPONLY = False  # Для разрешения работы с куки в браузере

# Stripe settings
STRIPE_PUBLISHABLE_KEY = config("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")
STRIPE_API_VERSION = config("STRIPE_API_VERSION")
STRIPE_WEBHOOK_SECRET = config("STRIPE_WEBHOOK_SECRET")

# Настройки для ЮKассы
SHOP_ID = config("SHOP_ID")
KASSA_SECRET_KEY = config("KASSA_SECRET_KEY")

from yookassa import Configuration
Configuration.configure(SHOP_ID, KASSA_SECRET_KEY)


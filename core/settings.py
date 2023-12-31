import os
from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab

SECRET_KEY = "ro!3j3k2)$o@4iis+xbd"
DEBUG = True
ALLOWED_HOSTS = []
AUTH_USER_MODEL = "user.User"

HOST = "http://localhost:8000"

# Apps
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_yasg",
    "rest_framework_simplejwt",
    "channels",
    "django_celery_beat",
    "corsheaders",

    # apps
    "user",

    "task",
    "task.document",
    "task.image",

    "upload",

    # APIs
    "api.v1.user_auth",

    "api.v1.task",
    "api.v1.task.conversion",
    "api.v1.task.ocr",
    "api.v1.upload",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# REST configuration
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ]
}

ROOT_URLCONF = "core.urls"
BASE_DIR = Path(__file__).resolve().parent.parent

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# Application
WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"

# Databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
# JWT authentication
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
}

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# CORS
CORS_ALLOW_ALL_ORIGINS = True

# Static and media folders
STATIC_URL = "static_root/"
STATIC_ROOT = BASE_DIR.joinpath(STATIC_URL)

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR.joinpath(MEDIA_URL)

# Misc
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Swagger
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "api_key": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization"
        }
    },
}

# Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

# Celery settings
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:6379"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

CELERY_BEAT_SCHEDULE = {
    "cancel_stale_tasks": {
        "task": "task.periodical.cancel_stale_tasks",
        "schedule": crontab(minute="*/1"),
    },
}

# Stale age
STALE_TASK_AGE = 3 * 60 # in seconds

# Upload file size limit
MAX_FILE_UPLOAD_SIZE = 1024 * 1024 * 100 # 100Megabytes

# Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, 6379)],
        },
    },
}

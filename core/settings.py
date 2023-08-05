import os
from pathlib import Path

from celery.schedules import crontab

SECRET_KEY = "django-insecure-o$@x3xk^on2&zq+*g0^$0zih+m2ljnro!3j3k2)$o@4iis+xbd"
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
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
    "channels",
    "django_celery_beat",
    "corsheaders",

    # apps
    "user",

    "task",
    "task.document",
    "task.image",

    "clipboard",

    # APIs
    "api.v1.user_auth",

    "api.v1.task",
    "api.v1.task.document",
    "api.v1.task.image",

    "api.v1.clipboard",
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
        "rest_framework.authentication.TokenAuthentication"
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
STALE_TASK_AGE = 1 * 60 * 20  # in seconds
CLIPBOARD_MEDIA_AGE = 30  # in days

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

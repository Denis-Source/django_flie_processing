from pathlib import Path

SECRET_KEY = "django-insecure-o$@x3xk^on2&zq+*g0^$0zih+m2ljnro!3j3k2)$o@4iis+xbd"
DEBUG = True
ALLOWED_HOSTS = []
AUTH_USER_MODEL = "user.User"

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

    "user",
    "log_record",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
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
WSGI_APPLICATION = "core.wsgi.application"

# Database
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

# Static and media folders
STATIC_URL = "static_root/"
STATIC_ROOT = BASE_DIR.joinpath(STATIC_URL)

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR.joinpath(MEDIA_URL)

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} {levelname} {module} {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose"
        },
        "log_record_handler": {
            "class": "log_record.handlers.LogRecordHandler",
            "formatter": "verbose",
        }
    },
    "root": {
        "handlers": ["console", "log_record_handler"],
        "level": "DEBUG",

    },
    "loggers": {
        "django": {
            "handlers": ["console", "log_record_handler"],
            "level": "ERROR",
        }
    },
}

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
import os
from pathlib import Path
from dotenv import load_dotenv
from corsheaders.defaults import default_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Carrega as variáveis do arquivo .env
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG")

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    ADMINS = [(os.getenv("SUPER_USER"), os.getenv("EMAIL"))]
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# ALLOWED_HOSTS = [os.environ.get("ALLOWED_HOSTS")]
ALLOWED_HOSTS = ["*", "localhost", "127.0.0.1"]

CORS_ALLOW_HEADERS = list(default_headers) + [
    "X-Register",
]

# CORS Config
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # apps próprios
    "apps.base",
    "apps.cliente",
    "apps.produto",
    "apps.pedido",
    # terceiros
    "corsheaders",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.instagram",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "requestlogs.middleware.RequestLogsMiddleware",
]

MIDDLEWARE_CLASSES = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django_session_timeout.middleware.SessionTimeoutMiddleware",
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1

# timeout tempo de inatividate no sistema
SESSION_EXPIRE_SECONDS = 1800
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
# SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = 60
SESSION_TIMEOUT_REDIRECT = "http://localhost:8000/"

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "requestlogs.views.exception_handler",
}

ROOT_URLCONF = "core.urls"

# Logs
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "requestlogs_to_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "info.log",
        },
    },
    "loggers": {
        "requestlogs": {
            "handlers": ["requestlogs_to_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

REQUESTLOGS = {
    "SECRETS": ["password", "token"],
    "METHODS": ("PUT", "PATCH", "POST", "DELETE"),
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Apps
                # "core.context_processors.context_social",
                # "core.context_processors.context_sacola",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

SOCIALACCOUNT_PROVIDERS = {
    "facebook": {
        "METHOD": "oauth2",
        "SCOPE": ["email"],
        "AUTH_PARAMS": {"auth_type": "reauthenticate"},
        "INIT_PARAMS": {"cookie": True},
        "FIELDS": ["id", "email", "name", "first_name", "last_name"],
        "EXCHANGE_TOKEN": True,
        "LOCALE_FUNC": lambda request: "pt_BR",
        "VERIFIED_EMAIL": False,
        "VERSION": "v7.0",
    },
    "instagram": {
        "APP": {
            "client_id": "<YOUR_INSTAGRAM_CLIENT_ID>",
            "secret": "<YOUR_INSTAGRAM_CLIENT_SECRET>",
        }
    },
}

# Database
# https://docs.djangobase.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

db_name = os.getenv("NAME_DB")

if db_name is None:
    raise ValueError("A variável de ambiente NAME_DB não está definida ou é inválida")


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, db_name),
        "USER": os.getenv("USER_DB"),
        "PASSWORD": os.getenv("PASSWORD_DB"),
        "HOST": os.getenv("HOST_DB"),
        "PORT": os.getenv("PORT_DB"),
    }
}

# Password validation
# https://docs.djangobase.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangobase.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangobase.com/en/4.1/howto/static-files/

STATIC_DIR = os.path.join(BASE_DIR, "static")
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = DEFAULT_FROM_EMAIL

LOGIN_URL = "/"
LOGOUT_URL = "/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# --- Messages --- #
from django.contrib.messages import constants

MESSAGE_TAGS = {
    constants.ERROR: "alert-danger",
    constants.WARNING: "alert-warning",
    constants.DEBUG: "alert-info",
    constants.SUCCESS: "alert-success",
    constants.INFO: "alert-info",
}

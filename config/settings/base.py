import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def env_bool(key: str, default: bool = False) -> bool:
    val = os.environ.get(key)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-dev-key-change-me")
DEBUG = env_bool("DEBUG", False)
ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if h.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.companies",
    "apps.core",
    "apps.dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "apps.core.middleware.ImpersonationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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
                "apps.core.context_processors.impersonation",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

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

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "core.CustomUser"
LOGIN_URL = "core:login"
LOGOUT_REDIRECT_URL = "core:login"


def _database_config():
    engine = os.environ.get(
        "DB_ENGINE",
        "django.db.backends.sqlite3",
    )
    name = os.environ.get("DB_NAME", "db.sqlite3")

    config: dict = {
        "ENGINE": engine,
        "NAME": name,
    }

    if engine == "django.db.backends.sqlite3":
        if not Path(name).is_absolute():
            config["NAME"] = str(BASE_DIR / name)

    if engine == "django.db.backends.mysql":
        config["USER"] = os.environ.get("DB_USER", "")
        config["PASSWORD"] = os.environ.get("DB_PASSWORD", "")
        config["HOST"] = os.environ.get("DB_HOST", "localhost")
        config["PORT"] = os.environ.get("DB_PORT", "3306")
        options_raw = os.environ.get("DB_OPTIONS_JSON", "{}")
        try:
            config["OPTIONS"] = json.loads(options_raw) if options_raw else {}
        except json.JSONDecodeError:
            config["OPTIONS"] = {}

    return config


DATABASES = {
    "default": _database_config(),
}

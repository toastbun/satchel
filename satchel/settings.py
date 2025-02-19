"""
Django settings for satchel project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path


BASE_DIR = (
    Path(__file__).resolve().parent.parent
)  # Build paths inside the project like this: BASE_DIR / 'subdir'.


# read environment variables
DEBUG = os.environ.get("SATCHEL_DEBUG", False)
SECRET_KEY = os.environ.get("SECRET_KEY")
THEME = os.environ.get("DEFAULT_THEME", "light")


ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",  # top
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "base.apps.BaseConfig",
    "pantry.apps.PantryConfig",
    "bulma",  # added
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # added
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "satchel.urls"


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
                "utils.context_processors.theme_context",
            ],
        },
    },
]


WSGI_APPLICATION = "satchel.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "satcheldb",
        "USER": os.environ.get("SATCHEL_DB_USERNAME"),
        "PASSWORD": os.environ.get("SATCHEL_DB_PASSWORD"),
        "HOST": "127.0.0.1",
        "PORT": "5432",
   }
}


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
TIME_ZONE = "America/Chicago"
USE_I18N = True
USE_TZ = True


STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


"""
    Make sure that each app/static/ directory includes a redundant app/ folder.

    For example, when creating a main.css file,

    #   INCORRECT:  /app/static/css/main.css
    #   CORRECT:    /app/static/app/css/main.css
"""

STATIC_URL = "static/"  # url alias for referencing collected static files stored in the STATIC_ROOT
STATIC_ROOT = (BASE_DIR / "staticfiles")  # the folder into which static files are collected

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


SESSION_EXPIRE_AT_BROWSER_CLOSE = True

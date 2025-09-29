"""
Django settings for marketcampus project.
"""

import os
from pathlib import Path

# CORREGIR: Solo una definición de BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ELIMINAR esta línea duplicada:
# BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-dur(lvom&15#12yqnf4j+1=8f0yf4q3(u7g@kifnv9&7ghz+8c'
DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    ## apps
    'usuarios',
    'productos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'marketcampus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ← ESTÁ BIEN
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # CORREGIR: Agregar estos context processors que faltan
                'django.template.context_processors.debug',  # ← FALTABA
                'django.template.context_processors.request',  # ← FALTABA
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'marketcampus.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DEBUG TEMPORAL - Agrega esto al final para verificar
print("=== DEBUG TEMPLATES ===")
print("BASE_DIR:", BASE_DIR)
print("Templates path:", BASE_DIR / 'templates')
print("Templates exists:", (BASE_DIR / 'templates').exists())
if (BASE_DIR / 'templates').exists():
    template_dir = BASE_DIR / 'templates'
    print("Contents of templates/:")
    for item in template_dir.iterdir():
        print(f"  - {item.name}")
        if item.is_dir():
            for subitem in item.iterdir():
                print(f"    - {subitem.name}")
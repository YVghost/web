"""
Django settings for marketcampus project.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dur(lvom&15#12yqnf4j+1=8f0yf4q3(u7g@kifnv9&7ghz+8c'

# SECURITY WARNING: don't run with debug turned on in production!
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

    # Third party apps
    'imagekit',

    # Local apps
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
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',  # Para usar {{ MEDIA_URL }}
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
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'es-es'  # Cambiado a español
TIME_ZONE = 'America/Guayaquil'  # Zona horaria de Ecuador
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Media files (Uploaded by users)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings
LOGIN_REDIRECT_URL = 'productos:explorar'  # Después de login exitoso
LOGIN_URL = 'login'  # URL para redireccionar cuando se requiere login
LOGOUT_REDIRECT_URL = 'productos:explorar'  # Después de logout

# Email configuration (para desarrollo)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB

# ImageKit configuration (para procesamiento de imágenes)
IMAGEKIT_DEFAULT_IMAGE_CACHE_BACKEND = 'imagekit.imagecache.NonValidatingImageCacheBackend'
IMAGEKIT_CACHEFILE_DIR = 'CACHE/images'
IMAGEKIT_DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Security settings (para desarrollo - revisar en producción)
SESSION_COOKIE_SECURE = False  # True en producción con HTTPS
CSRF_COOKIE_SECURE = False     # True en producción con HTTPS
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Debug template verification (puedes eliminar esto en producción)
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
# Example Django Settings Configuration

# Add this to your main Django project's settings.py

# ============================================
# INSTALLED APPS
# ============================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Your app
    'WEATHERAPP',
]

# ============================================
# MIDDLEWARE
# ============================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ============================================
# TEMPLATES
# ============================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Add your template directories here
        'APP_DIRS': True,  # This enables app template discovery
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ============================================
# DATABASE
# ============================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

# For PostgreSQL (recommended for production):
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'weatherapp_db',
#         'USER': 'your_db_user',
#         'PASSWORD': 'your_db_password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# ============================================
# SECURITY
# ============================================

DEBUG = True  # Set to False in production

ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Add your domain in production

# ============================================
# STATIC AND MEDIA FILES
# ============================================

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = 'media'

# ============================================
# LOGGING
# ============================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

# ============================================
# REQUESTS (for API calls)
# ============================================

# You can add request timeout settings here
REQUEST_TIMEOUT = 5  # seconds

# ============================================
# ENVIRONMENT VARIABLES (Best Practice)
# ============================================

# Use python-dotenv to load from .env file:
# pip install python-dotenv

from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Then in views.py:
# API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY')

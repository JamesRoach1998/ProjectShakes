# Enable debug mode for development
DEBUG = True

# Allow your local server
ALLOWED_HOSTS = []

import os

# Set ESPEAK_PATH to the Homebrew-installed espeak binary
os.environ['ESPEAK_PATH'] = '/opt/homebrew/bin/espeak'

# Optionally also ensure PATH includes the directory
os.environ['PATH'] = '/opt/homebrew/bin:' + os.environ.get('PATH', '')


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',   # ✅ REQUIRED
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # ✅ REQUIRED
    'django.contrib.messages.middleware.MessageMiddleware',      # ✅ REQUIRED
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'translator',  # Your app
]

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # ← this line
        'APP_DIRS': True,
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


STATIC_URL = '/static/'
ROOT_URLCONF = 'shakes.urls'
SECRET_KEY = 'django-insecure-3a#2v=un^+d@evx4zr=*mq49c5&@v4a*7c#q1gf6qz3o(lom87'

ALLOWED_HOSTS = [
  "localhost",
  "127.0.0.1",
  "projectshakes-production.up.railway.app",
]


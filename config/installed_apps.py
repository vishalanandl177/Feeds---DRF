# Application definition

DJANGO_INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'rest_framework_swagger',
]

MY_APP = [
    'user',
    'feed',
]

INSTALLED_APPS = MY_APP + DJANGO_INSTALLED_APPS

"""
Django settings for Sell_Web project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#import sae.const
#
#MYSQL_DB = sae.const.MYSQL_DB 
#MYSQL_USER = sae.const.MYSQL_USER 
#MYSQL_PASS = sae.const.MYSQL_PASS 
#MYSQL_HOST_M = sae.const.MYSQL_HOST 
#MYSQL_HOST_S = sae.const.MYSQL_HOST_S 
#MYSQL_PORT = sae.const.MYSQL_PORT

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3u4h!f61-9%_xyb!*r5qwppaz$ihllx+ree@&h8)ov+uq6!k68'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

#settings.py

##email 
#EMAIL_HOST = 'smtp.sina.com'                   
#EMAIL_PORT = 25                                 
#EMAIL_HOST_USER = 'sommerce_shop@sina.com'      
#EMAIL_HOST_PASSWORD = '1234567890'                 
#EMAIL_SUBJECT_PREFIX = u'[Sommerce Shop]'           
#EMAIL_USE_TLS = True                           
##admin
#SERVER_EMAIL = 'lyd_study@163.com'          
## Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Sellapp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Sell_Web.urls'

WSGI_APPLICATION = 'Sell_Web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'SellWeb_mysql',    
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '',
        'PORT': '3306',

    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
TEMPLATE_DIRS = (
'./Sellapp/template/',
)

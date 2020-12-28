"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
# from v1.commonapp.views.secretcache import SecretManager
# secret = SecretManager()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4urz*1-p45#e2nnlg$fjqb*rhv^w_l35n4#^l%m^8$*2t5slpg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_twilio',
    'rest_framework',
    'storages',
    'corsheaders',
    'django_filters',
    'django_crontab',
    'master',
    'v1.asset',
    'v1.billing',
    'v1.campaign',
    'v1.commonapp',
    'v1.consumer',
    'v1.complaint',
    'v1.service',
    'v1.contract',
    'v1.employee',
    'v1.meter_data_management',
    'v1.payment',
    'v1.payroll',
    'v1.registration',
    'v1.request',
    'v1.store',
    'v1.supplier',
    'v1.survey',
    'v1.userapp',
    'v1.tender',
    'v1.work_order',
    'v1.utility',
    'v1.tenant',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api.urls'

AUTH_USER_MODEL = 'master.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

WSGI_APPLICATION = 'api.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'smart360_2',
        'USER': 'postgres',
        'PASSWORD': 'chinmay123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DISPLAY_DATE_FORMAT = "%d-%b-%Y"

DISPLAY_DATE_TIME_FORMAT = "%d/%m/%Y %H:%M:%S"

INPUT_DATE_FORMAT = "%d-%b-%Y"

CORS_ORIGIN_ALLOW_ALL = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'



# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': BASE_DIR + '/debug.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'INFO',
#         },
#     },
# }

# CELERY STUFF
BROKER_URL = 'redis://localhost:6379'  # Todo redis broker is use for message transform
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json', 'application/x-python-serialize']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'

# Cronjob configuration
CRONJOBS = [
    ('*/1 * * * *', 'v1.meter_data_management.task.validation_assignment.assign_validation', '>> /home/aki/Aki/Projects/Smart360-app/api/validation.log'),
    ('0 */30 * * *', 'meter_data_management.task.bill_distribution.import_bill_distribution_data', '>> /home/aki/Aki/Projects/Smart360-app/api/bill_distribution.log')
]

# Amazon s3 Configuration
# AWS_ACCESS_KEY_ID = ''
# AWS_SECRET_ACCESS_KEY = ''
# AWS_STORAGE_BUCKET_NAME = ''
# AWS_S3_ENDPOINT_URL = ''
# AWS_DEFAULT_ACL = None
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }
# AWS_LOCATION = ''
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# MEDIA_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)


# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'

# SMS configuration
TWILIO_ACCOUNT_SID = 'ACf8545f63b2bf3513b90b2ac626b53d8b'
TWILIO_AUTH_TOKEN = '413b55d88e459cc05c713b4510808dec'

# Django settings for odonto project.
import os
import sys

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

try:
    import dj_database_url

    DATABASES = {
        'default': dj_database_url.config(default='sqlite:///' + PROJECT_PATH + '/opal.sqlite')
    }
except ImportError:
    if os.environ.get('GITHUB_WORKFLOW'):
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'ci_db_test',
                'USER': 'postgres',
                'PASSWORD': 'postgres',
                'HOST': 'localhost',
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(PROJECT_PATH, 'opal.sqlite'),
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': ''
            }
        }


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.herokuapp.com',
    'ntghcomdent1',
    'ntghcomdent2',
]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, 'assets')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/assets/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '%c856+vs+9q*l-^zz6%z_frd9t+r(7ii&kb5pqgnwk5_6qc+@6'

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'opal.middleware.AngularCSRFRename',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'opal.middleware.DjangoReversionWorkaround',
    'reversion.middleware.RevisionMiddleware',
    'odonto.middleware.logging_middleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'odonto.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'odonto.wsgi.application'
HOST_NAME_AND_PROTOCOL = "http://ntghcomdent1"



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_PATH, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'opal.context_processors.settings',
                'opal.context_processors.models',
                'opal.core.pathway.context_processors.pathways',
                'odonto.context_processors.odonto_roles',
                'odonto.context_processors.episode_counts',
            ],
        },
    },
]


if not DEBUG:
    # Cache templates in production
    TEMPLATES[0]['OPTIONS']['loaders'] = [(
        'django.template.loaders.cached.Loader',
        TEMPLATES[0]['OPTIONS']['loaders'],
    )]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'axes',
    'reversion',
    'rest_framework',
    'rest_framework.authtoken',
    'compressor',
    'odontotheme',
    'opal',
    'opal.core.search',
    'opal.core.pathway',
    'odonto',
    'odonto.odonto_submissions',
    'django.contrib.humanize',
    'passwordreset',
    'django.contrib.admin',
    'plugins.add_patient_step',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
V_FORMAT = '%(asctime)s %(process)d %(thread)d %(filename)s %(funcName)s \
%(levelname)s %(message)s'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': V_FORMAT
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'filters': [],
            'class': 'logging.StreamHandler',
        },
        'console_detailed': {
            'level': 'INFO',
            'filters': [],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'opal.core.log.ConfidentialEmailer'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'odonto.requestLogger': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'error_emailer': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'odonto_submissions': {
            'handlers': ['console_detailed', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

# Begins custom settings

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATE_FORMAT = 'd/m/Y'
DATE_INPUT_FORMATS = ['%d/%m/%Y']
DATETIME_FORMAT = 'd/m/Y H:i:s'
DATETIME_INPUT_FORMATS = ['%d/%m/%Y %H:%M:%S']
TIME_FORMAT = "H:i:s"

CSRF_COOKIE_NAME = 'XSRF-TOKEN'
APPEND_SLASH = False

AXES_LOCK_OUT_AT_FAILURE = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
if not DEBUG:
    EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME', '')
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD', '')
else:
    EMAIL_PORT = 1025
    EMAIL_HOST = 'localhost'

COVERAGE_EXCLUDE_MODULES = ('odonto.migrations', 'odonto.tests',
                            'odonto.local_settings',
                            'opal.migrations', 'opal.tests',
                            'opal.wsgi')


# Begins OPAL Settings

OPAL_LOG_OUT_MINUTES = 30
OPAL_LOG_OUT_DURATION = OPAL_LOG_OUT_MINUTES *60 *1000

# Begins OPAL optional settings
# OPAL_EXTRA_HEADER = ''
# OPAL_EXTRA_APPLICATION = ''

# Uncomment this to swap out the logo used by this application
# OPAL_LOGO_PATH = 'img/ohc-trans.png'

# Uncomment this if you want to implement custom dynamic flows.
# OPAL_FLOW_SERVICE = 'AppFlow'

# Enable/Disable autocomplete from navbar search
OPAL_AUTOCOMPLETE_SEARCH = False

OPAL_DEFAULT_SEARCH_FIELDS = [
    "demographics__nhs_number",
    "demographics__first_name",
    "demographics__surname"
]

INTEGRATING = False

# OPAL required Django settings you should edit

CONTACT_EMAIL = []
DEFAULT_FROM_EMAIL = 'hello@example.com'
DEFAULT_DOMAIN = 'http://openodonto.com/'

# Begins OPAL Settings you should edit !

OPAL_BRAND_NAME = 'Open Odonto'
VERSION_NUMBER = '0.60.0'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

ODONTO_LOGIN_MESSAGE = 'Log in to get started'

# if you want sass, uncomment the below and gem install sass
# COMPRESS_PRECOMPILERS = (
#     ('text/x-scss', 'sass --scss {infile} {outfile}'),
# )

# <---- DPB Credentials
DPB_USERNAME = None
DPB_PASSWORD = None
DPB_SITE_ID = "89651"

SEND_MESSAGES = False
LOCATION = 10108
DESTINATION = "A0DPB"
# These used to be different but are now the same.
FP17_CONTRACT_NUMBER = 1021700000
FP17O_CONTRACT_NUMBER = 1021700000
# DPB Credentials ------>

# Requests does not use the server cert certificates so pass them in
SSH_CERTS = ""

# above this the email about the daily submissins will say URGENT
FAILED_TO_SEND_WARNING_THRESHOLD = 6


# always decline the patient email/phone when sending down stream
ALWAYS_DECLINE_EMAIL_PHONE = True

SHOW_RECORD_PANELS = False

try:
    from odonto.local_settings import *
except ImportError:
    pass

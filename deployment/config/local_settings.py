# we use postgres in production
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'odonto',
    'USER': 'ohc',
    'PASSWORD': 'Nope',
    'HOST': 'localhost',
    'PORT': '5432',
  }
}

"""
FP17_CONTRACT_NUMBER = 1946890001
FP17O_CONTRACT_NUMBER = 1946890002
"""

FP17_CONTRACT_NUMBER = 1021700000
FP17O_CONTRACT_NUMBER = 1021700000

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'ntghcomdent1',
    'ntghcomdent2',
]




OPAL_ANALYTICS_ID = 'UA-35112560-16'
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "10.138.0.159"
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = "ohcsupport@northumbria-healthcare.nhs.uk"
SECRET_KEY = 'changeTasdfasdfhisToo'
DEBUG = False
ADMINS = [('support', 'support@openhealthcare.org.uk',)]
'PROXY = {"https": "https://10.138.41.165:8080"}'
SSH_CERTS = '/usr/lib/ohc/etc/ca-certificates.crt'

SEND_MESSAGES = True
DPB_USERNAME = "20190517123156417"
DPB_PASSWORD = "Wf>281!qdV!K"

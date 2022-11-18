import os
import secrets
from celery.schedules import crontab

MAIL_SERVER ='smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'flasksender1912@gmail.com'
MAIL_DEFAULT_SENDER = 'flasksender1912@gmail.com'
MAIL_PASSWORD = '!!!!!!!!'
MAIL_USE_TLS = False
MAIL_USE_SSL = True

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_BACKEND = 'redis://localhost:6379/0'
CELERYBEAT_SCHEDULE = {
    'test-celery': {
        'task': 'send_mail',
        # Every minute
        'schedule': crontab(minute="*"),
    }
}
CELERY_TIMEZONE = 'Asia/Kolkata'

DEBUG= True
SQLALCHEMY_DATABASE_URI = 'sqlite:///anica.sqlite3'
SECRET_KEY= os.environ.get("SECRET_KEY", "bubla")
salt=str(secrets.SystemRandom().getrandbits(128))
SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", salt)
SQLALCHEMY_TRACK_MODIFICATIONS=False

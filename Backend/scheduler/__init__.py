from celery import Celery
from flask import Flask
from celery.schedules import crontab
from api import send_daily_email, send_monthly_email
def make_celery(app): # create context tasks in celery
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_BACKEND'] = 'redis://localhost:6379/0'
app.config['CELERY_TIMEZONE'] = 'Asia/Kolkata'
app.config['CELERYBEAT_SCHEDULE'] = {
    'every-month': {
        'task': 'send_monthly_mail',
        'schedule': crontab(minute=*""),
    },
    'every-day': {
        'task': 'send_daily_mail',
        'schedule': crontab(minute=0, hour=9), #9 AM 
    }
}

celery_app = make_celery(app)

@celery_app.task(name="send_monthly_mail")
def send_monthly_mail():
    res = send_monthly_email()
    print(res)
    return "Monthly!"

@celery_app.task(name="send_daily_mail")
def send_daily_mail():
    res = send_daily_email()
    print(res)
    return "Daily!"



from app import flask_app
from celery.schedules import crontab

celery_app = flask_app.extensions['celery']

celery_app.conf.imports = ['app.tasks.tasks']

celery_app.conf.beat_schedule = {
    'daily-task': {
        'task': 'app.tasks.check_outdate_schedule_share',
        'schedule': crontab(hour=0)
    },
}

app = celery_app

if __name__ == '__main__':
    app.start()
from flask import Flask
from celery import Celery, Task


def celery_init_app(app: Flask):
    class ContextTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(
        app.name,
        task_cls=ContextTask,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    # celery_app.config_from_object(app.config['CELERY_CONFIG'])
    celery_app.conf.update({'task_serializer': 'json',
        'accept_content': ['json'],
        'result_serializer': 'json',
        'timezone': 'Asia/Ho_Chi_Minh'})
    app.extensions['celery'] = celery_app
    return celery_app
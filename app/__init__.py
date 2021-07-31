from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config,DevelopmentConfig, Config
from celery import Celery
from elasticsearch import Elasticsearch



import os
basedir = os.path.abspath(os.path.dirname(__file__))


db = SQLAlchemy()
def page_not_found(e):
    return render_template('404.html'), 404

def internal_server_error(e):
    return render_template('500.html'), 500

def make_celery(app_name=__name__):
    return Celery(app_name, backend='db+sqlite:///' + os.path.join(basedir, 'data.sqlite'),broker=Config.CELERY_BROKER_URL)
def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.
    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name)
    celery.conf.update(app.config.get('CELERY_CONFIG', {}))
    celery.conf.beat_schedule = {
        'scrape-twit-every-5-minutes': {
            'task': 'app.main.tasks.run_async_parser',
            'schedule': 300.0
        }
    }
    celery.conf.timezone = 'UTC'
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_app():
    app = Flask(__name__,
                static_url_path='',
                static_folder='static',
                template_folder='templates')
    app.config.from_object(DevelopmentConfig)
    DevelopmentConfig.init_app(app)
    migrate = Migrate(app, db)
    db.init_app(app)
    migrate.init_app(app)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None



    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)
    return app

celery = create_celery_app()
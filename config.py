import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or "http://localhost:9200/"
    POSTS_PER_PAGE = 25
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TWIT_USER = os.environ.get('TWIT_USER')
    TWIT_PASS = os.environ.get('TWIT_PASS')
    TWIT_API_KEY = os.environ.get('TWIT_API_KEY')
    TWIT_API_SECRET = os.environ.get('TWIT_API_SECRET')
    TWIT_API_TOKEN = os.environ.get('TWIT_API_TOKEN')
    TWIT_API_SECRET_TOKEN = os.environ.get('TWIT_API_SECRET_TOKEN')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    result_backend = 'db+sqlite:///' + os.path.join(basedir, 'data.sqlite')
    CELERY_CONFIG = {
        'broker_url': REDIS_URL,
        'result_backend': REDIS_URL,
        'timezone': 'UTC',
        'include': [
            'app.main.tasks'
        ]
    }
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')



    @staticmethod
    def init_app(app):
        pass
class DevelopmentConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
        'development': DevelopmentConfig,
        'default': DevelopmentConfig
        }
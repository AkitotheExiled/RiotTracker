from app import create_celery_app
from app.main.twitter_parser.parser import run_parser

celery = create_celery_app()
@celery.task
def run_async_parser():
    run_parser()
    return None

@celery.task
def print_msg(msg):
    print(msg)

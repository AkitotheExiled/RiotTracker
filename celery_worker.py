import os
from app import create_celery_app, create_app

from app import DevelopmentConfig

app = create_app()
create_celery_app()
app.app_context().push()
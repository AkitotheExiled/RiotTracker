web: flask db upgrade; gunicorn app:app;
worker: python celery_worker.py celery worker --loglevel=info
celery_beat: python celery_worker.py celery beat --loglevel=info
web: env > .env; env PYTHONUNBUFFERED=true honcho start -f Procfile.real 2>&1

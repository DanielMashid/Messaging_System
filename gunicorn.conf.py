import os

name = os.getenv("GUNICORN_NAME", "messages-handler")
workers = os.getenv("GUNICORN_WORKERS", 2)
threads = os.getenv("GUNICORN_THREADS", 4)
worker_class = 'gthread'
worker_tmp_dir = "/dev/shm"
loglevel = os.getenv("LOG_LEVEL", "info")
limit_request_line = 0
bind = '0.0.0.0:8000'

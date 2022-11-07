release: python manage.py migrate
web: gunicorn --bind :$PORT messages_handler.wsgi

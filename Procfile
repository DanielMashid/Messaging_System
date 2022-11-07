release: python manage.py migrate
web: gunicorn messaging-system.wsg:application --log-file--
web: python server/manage.py runserver 0.0.0.0:$PORT

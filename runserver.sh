# /bin/bash

source env/bin/activate
python manage.py runserver 0.0.0.0:8000

# gunicorn -c conf/gunicorn_config.py config.wsgi
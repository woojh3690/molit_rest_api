nohup gunicorn --workers 4 --thread 9 --timeout=600 --bind 0.0.0.0:8000 rest_api_main:app > server.log &

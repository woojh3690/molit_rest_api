nohup gunicorn --workers 4 --thread 9 --timeout=600 --bind 0.0.0.0:8000 rest_api_main:app > server.log&
nohup gunicorn --keyfile ../conf/emqx.key --certfile ../conf/emqx.pem --workers 4 --thread 9 --timeout=600 --bind 0.0.0.0:8001 rest_api_main:app > server_tls.log&

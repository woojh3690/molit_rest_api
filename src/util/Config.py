import yaml

class BasicApiConfig:
    _log_path = 0
    _log_level = 0

    def __init__(self, log_path, log_level):
        self._log_path = log_path
        self._log_level = log_level

class RestApiKeyConfig:
    _db_ip = 0
    _db_port = 0
    _db_id = 0
    _db_passwd = 0
    _db_name = 0
    _select_sql = 0

    def __init__(self, db_ip, db_port, db_id, db_passwd, db_name, select_sql):
        self._db_ip = db_ip
        self._db_port = db_port
        self._db_id = db_id
        self._db_passwd = db_passwd
        self._db_name = db_name
        self._select_sql = select_sql

class KafkaConfig:
    _topic_name = 0
    _bootstrap_servers = 0
    _timeout_ms = 0

    def __init__(self, topic_name, bootstrap_servers, timeout_ms):
        self._topic_name = topic_name
        self._bootstrap_servers = bootstrap_servers
        self._timeout_ms = timeout_ms

class RabbitMQRpcConfig:
    _user_name = 0
    _user_passwd = 0
    _host = 0
    _port = 0
    _virtual_host = 0

    def __init__(self, user_name, user_passwd, host, port, virtual_host):
        self._user_name = user_name
        self._user_passwd = user_passwd
        self._host = host
        self._port = port
        self._virtual_host = virtual_host

class RestApiCrawlConfig:
    _basic_api_config = 0
    _rest_api_key_dict = 0
    _kafka_producer_config = 0

    def __init__(self, basic_api_config, rest_api_key_dict, rest_api_crawl_obj):
        self._basic_api_config = basic_api_config
        self._rest_api_key_dict = rest_api_key_dict
        kafka_producer_obj = rest_api_crawl_obj['kafka_producer_config']
        self._kafka_producer_config = KafkaConfig(kafka_producer_obj['topic_name'], kafka_producer_obj['bootstrap_servers'], kafka_producer_obj['timeout_ms'])

class RestApiSelConfig:
    _basic_api_config = 0
    _rest_api_key_dict = 0
    _kafka_producer_config = 0
    _kafka_consumer_config = 0
    _rabbitmq_rpc_config = 0

    def __init__(self, basic_api_config, rest_api_key_dict, rest_api_sel_obj):
        self._basic_api_config = basic_api_config
        self._rest_api_key_dict = rest_api_key_dict
        kafka_producer_obj = rest_api_sel_obj['kafka_producer_config']
        self._kafka_producer_config = KafkaConfig(kafka_producer_obj['topic_name'], kafka_producer_obj['bootstrap_servers'], kafka_producer_obj['timeout_ms'])
        kafka_consumer_obj = rest_api_sel_obj['kafka_consumer_config']
        self._kafka_consumer_config = KafkaConfig(kafka_consumer_obj['topic_name'], kafka_consumer_obj['bootstrap_servers'], kafka_consumer_obj['timeout_ms'])
        rabbitmq_rpc_obj = rest_api_sel_obj['rabbitmq_config']
        self._rabbitmq_rpc_config = RabbitMQRpcConfig(rabbitmq_rpc_obj['user_name'], rabbitmq_rpc_obj['user_passwd'], rabbitmq_rpc_obj['host'], rabbitmq_rpc_obj['port'], rabbitmq_rpc_obj['virtual_host'])

class RestApiCmdConfig:
    _basic_api_config = 0
    _rest_api_key_dict = 0
    _kafka_producer_config = 0
    _kafka_consumer_config = 0
    _rabbitmq_rpc_config = 0

    def __init__(self, basic_api_config, rest_api_key_dict, rest_api_cmd_obj):
        self._basic_api_config = basic_api_config
        self._rest_api_key_dict = rest_api_key_dict
        kafka_producer_obj = rest_api_cmd_obj['kafka_producer_config']
        self._kafka_producer_config = KafkaConfig(kafka_producer_obj['topic_name'], kafka_producer_obj['bootstrap_servers'], kafka_producer_obj['timeout_ms'])
        kafka_consumer_obj = rest_api_cmd_obj['kafka_consumer_config']
        self._kafka_consumer_config = KafkaConfig(kafka_consumer_obj['topic_name'], kafka_consumer_obj['bootstrap_servers'], kafka_consumer_obj['timeout_ms'])
        rabbitmq_rpc_obj = rest_api_cmd_obj['rabbitmq_config']
        self._rabbitmq_rpc_config = RabbitMQRpcConfig(rabbitmq_rpc_obj['user_name'], rabbitmq_rpc_obj['user_passwd'], rabbitmq_rpc_obj['host'], rabbitmq_rpc_obj['port'], rabbitmq_rpc_obj['virtual_host'])

class RestApiUploadConfig:
    _basic_api_config = 0
    _rest_api_key_dict = 0
    _kafka_producer_config = 0
    _kafka_consumer_config = 0

    def __init__(self, basic_api_config, rest_api_key_dict, rest_api_upload_obj):
        self._basic_api_config = basic_api_config
        self._rest_api_key_dict = rest_api_key_dict
        kafka_producer_obj = rest_api_upload_obj['kafka_producer_config']
        self._kafka_producer_config = KafkaConfig(kafka_producer_obj['topic_name'], kafka_producer_obj['bootstrap_servers'], kafka_producer_obj['timeout_ms'])
        kafka_consumer_obj = rest_api_upload_obj['kafka_consumer_config']
        self._kafka_consumer_config = KafkaConfig(kafka_consumer_obj['topic_name'], kafka_consumer_obj['bootstrap_servers'], kafka_consumer_obj['timeout_ms'])

class RestApiTestConfig:
    _basic_api_config = 0
    _rest_api_key_dict = 0
    _kafka_producer_config = 0
    _kafka_consumer_config = 0

    def __init__(self, basic_api_config, rest_api_key_dict, rest_api_test_obj):
        self._basic_api_config = basic_api_config
        self._rest_api_key_dict = rest_api_key_dict
        kafka_producer_obj = rest_api_test_obj['kafka_producer_config']
        self._kafka_producer_config = KafkaConfig(kafka_producer_obj['topic_name'], kafka_producer_obj['bootstrap_servers'], kafka_producer_obj['timeout_ms'])
        kafka_consumer_obj = rest_api_test_obj['kafka_consumer_config']
        self._kafka_consumer_config = KafkaConfig(kafka_consumer_obj['topic_name'], kafka_consumer_obj['bootstrap_servers'], kafka_consumer_obj['timeout_ms'])

class Config:
    _config_path = 0
    _rest_api_basic_config = 0
    _rest_api_hdfs_jpype_config = 0
    _rest_api_key_config = 0
    _rest_api_crawl_config = 0
    _rest_api_sel_config = 0
    _rest_api_cmd_config = 0

    def __init__(self, config_path="/root/rest_api/conf/RestApiConfig.yaml"):
        self._config_path = config_path

    def load_rest_api_keys(self):
        return {'b3e23345f5711f7259b783b409c466de37de1bce764bb5fede023461fdefba47': 1}

    def load_config(self):
        with open(self._config_path, 'r') as f:
            config_obj = yaml.load(f, Loader=yaml.FullLoader)

        rest_api_basic_config_obj = config_obj['rest_api_basic_config']
        self._rest_api_basic_config = BasicApiConfig(rest_api_basic_config_obj['log_path'], rest_api_basic_config_obj['log_level'])
        rest_api_basic_config = self._rest_api_basic_config
    
        rest_api_key_dict = self.load_rest_api_keys()

        rest_api_crawl_obj = config_obj['rest_api_crawl_config']
        self._rest_api_crawl_config = RestApiCrawlConfig(rest_api_basic_config, rest_api_key_dict, rest_api_crawl_obj)

        rest_api_sel_obj = config_obj['rest_api_sel_config']
        self._rest_api_sel_config = RestApiSelConfig(rest_api_basic_config, rest_api_key_dict, rest_api_sel_obj)

        rest_api_cmd_obj = config_obj['rest_api_cmd_config']
        self._rest_api_cmd_config = RestApiCmdConfig(rest_api_basic_config, rest_api_key_dict, rest_api_cmd_obj)

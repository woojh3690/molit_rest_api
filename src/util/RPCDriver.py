import pika
import uuid

class RPCClient:

    def __init__(self, rpc_config):
        self.credentials = pika.PlainCredentials(username=rpc_config._user_name, password=rpc_config._user_passwd)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rpc_config._host, port=rpc_config._port, 
        virtual_host=rpc_config._virtual_host, credentials=self.credentials))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
    
    def send(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='RPC_QUEUE',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))

    def receive(self):
        while self.response is None:
            self.connection.process_data_events()

        return self.response

    def close(self):
        self.connection.close()
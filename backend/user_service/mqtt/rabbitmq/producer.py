##PRODUCER FOR API SIDE
##Exports a helper->instance of RabbitMQProducer
import json

import pika
from django.conf import settings
from pika.exceptions import AMQPError, NackError


class RabbitMQProducer:
    def __init__(self):
        params = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            heartbeat=600,
            blocked_connection_timeout=300,
            credentials=pika.PlainCredentials(
                username=settings.RABBITMQ_USERNAME,
                password=settings.RABBITMQ_PASSWORD
            ),
            #url_parameters=pika.URLParameters(settings.RABBITMQ_URL)
        )
        self.connection = pika.BlockingConnection(
            #pika.URLParameters(settings.RABBITMQ_URL),
            params
        )

        self.channel = self.connection.channel()
        
        self.channel.confirm_delivery() #accepts ACKs or NACKs
        
        self.channel.queue_declare(
            queue="mqtt_publish_queue",
            durable=True
        )
    def publish(self, message):
        self.channel.basic_publish(
            exchange="",
            routing_key="mqtt_publish_queue",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
    def close(self):
        self.connection.close()

def request_mqtt_publish(topic, payload):
    global producer
    message = {
                "action": "publish",
                "topic": topic,
                "payload": payload
                }
    try:
        producer.publish(message=message)
        
    except (AMQPError, NackError):
        producer = RabbitMQProducer()
        producer.publish(message=message)

producer = RabbitMQProducer()
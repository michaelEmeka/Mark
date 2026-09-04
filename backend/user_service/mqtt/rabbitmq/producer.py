##PRODUCER FOR API SIDE
##Exports a helper->instance of RabbitMQProducer
import json
import pika
from django.conf import settings

class RabbitMQProducer:
    def __init__(self):
        params = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            heartbeat=10,
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
    producer = RabbitMQProducer()

    producer.publish(
        {
            "action": "publish",
            "topic": topic,
            "payload": payload
        }
    )
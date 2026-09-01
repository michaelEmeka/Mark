##CONSUMER FOR MQTT WORKER SIDE
import json
import pika
from django.conf import settings

class RabbitMQConsumer:

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(settings.RABBITMQ_URL)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(
            queue="mqtt_publish_queue",
            durable=True
        )
    def consume(self, callback):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue="mqtt_publish_queue",
            on_message_callback=callback
        )
        print("Waiting for MQTT publish jobs...")
        self.channel.start_consuming()
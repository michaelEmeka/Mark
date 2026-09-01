from django.conf import settings
from awsiot import mqtt_connection_builder
from awscrt import mqtt
from .handlers import mqtt_message_handler
from .rabbitmq.consumer import RabbitMQConsumer
import json
import threading

class MQTTWorker:
    def __init__(self):
        self.connection = self.create_connection()

    def create_connection(self):
        print("Creating connection..")
        return mqtt_connection_builder.mtls_from_path(
            endpoint=str(settings.AWS_IOT_ENDPOINT),
            cert_filepath=str(settings.AWS_IOT_CERTIFICATE_PATH),
            pri_key_filepath=str(settings.AWS_IOT_PRIVATE_KEY_PATH),
            ca_filepath=str(settings.AWS_IOT_ROOT_CA_PATH),
            client_id=str(settings.MQTT_CLIENT_ID),
            clean_session=False,
            keep_alive_secs=30
        )
    def connect(self):
        print("Connecting to AWS IoT...")
        connect_future = self.connection.connect()
        print(connect_future.result())
        print("Connected to AWS IoT successfully")

    def on_message(self, topic, payload, **kwargs):
        print("\nMessage received!")
        #print("Topic: ", topic)
        #print("Payload: ", payload.decode("utf-8"))
        mqtt_message_handler(topic=topic, payload=payload)

    def publish(self, topic, payload):
        print(f"Sending message over mqtt.. to {topic}")
        #print(payload)
        try:
            payload = json.dumps(payload).encode("utf-8")
            result = self.connection.publish(
                topic=topic,
                payload=payload,
                qos=mqtt.QoS.AT_LEAST_ONCE
                )
            future = result[0]
            print(f"Message sent: {future.result()}")
        except Exception as e:
            print(f"Failed to publish MQTT message to {topic}: {e}")
            raise

    def subscribe(self):
        #Subscribing to events and status topics
        topics = ["attendance/device/+/events", "attendance/device/+/states"]

        for topic in topics:
            print(f"Subscribing to {topic}..")
            subscribe_future, _ = self.connection.subscribe(
                topic=topic,
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=self.on_message,
            )
            subscribe_future.result()
            print(f"Subscribed successfully to {subscribe_future}")

    def run(self):
        #running on main thread of the mqtt process
        self.connect()
        self.subscribe()

        #running rabbitMQ consumer on separate thread to avoid blocking
        rabbitmq_thread = threading.Thread(
            target=self.consume_publish_jobs,
            daemon=True
        )
        rabbitmq_thread.start()

        print("MQTT worker is listening for messages...")

        try:
            #keeping the main process alive
            while True:
                pass
        except KeyboardInterrupt:
            print("\nStopping MQTT worker...")
        

    def handle_publish_job(
            self,
            channel,
            method,
            properties,
            body
    ):
        try:
            message = json.loads(body)
            topic = message["topic"]
            payload = message["payload"]

            self.publish(
                topic=topic,
                payload=payload
            )

            channel.basic_ack(
                delivery_tag=method.delivery_tag
            )

        except Exception as error:
            print(f"Failed to process publish job: {error}")
            #rabbitmq redelivers failed jobs(uncacknowledged jobs)
    
    def consume_publish_jobs(self):
        print("Running rabbbitmq consumer on separate thread..")
        consumer = RabbitMQConsumer()
        consumer.consume(
            callback=self.handle_publish_job
        )
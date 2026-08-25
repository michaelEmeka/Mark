from django.conf import settings
from dotenv import load_dotenv
from awsiot import mqtt_connection_builder
from awscrt import mqtt
from .handlers import mqtt_message_handler
load_dotenv()

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


    def subscribe(self):
        #Subscribing to events and status topics
        topics = ["attendance/device/+/events", "attendance/device/+/status"]

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
        self.connect()
        self.subscribe()

        print("MQTT worker is listening for messages...")

        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("\nStopping MQTT worker...")
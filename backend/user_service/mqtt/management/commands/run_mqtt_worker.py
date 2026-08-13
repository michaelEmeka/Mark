from django.core.management.base import BaseCommand
from mqtt.client import MQTTWorker

class Command(BaseCommand):
    #"Starts the MQTT worker"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting MQTT worker...")

        worker = MQTTWorker()
        worker.run()

        self.stdout.write(
            self.style.SUCCESS("MQTT worker connected successfully")
        )
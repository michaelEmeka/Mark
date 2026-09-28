#pragma once

// Polls the fingerprint sensor; on a match either kicks off enrollment
// (ADMIN_ID) or queues a "fingerprint_scan" event for networkTask.
void fingerprintTask(void *parameter);

// Owns the MQTT/AWS IoT connection: reconnects on drop, pumps client.loop(),
// and drains networkQueue by publishing each EventRecord.
void networkTask(void *pvParameters);

// Drains displayQueue and renders each message on the OLED.
void displayTask(void *pvParameters);

// Handles SD-Card Utility
void loggingTask(void *pvParameters);
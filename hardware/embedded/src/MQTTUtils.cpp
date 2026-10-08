#include <ArduinoJson.h>

#include "MQTTUtils.h"
#include "Globals.h"
#include "SystemState.h"
#include "secrets.h"

char* generateEventId() {
    static char buf[40];
    snprintf(
        buf,
        sizeof(buf),
        "%08x-%04x-%04x-%04x-%08x%04x",
        (unsigned int)esp_random(),
        (unsigned int)(esp_random() & 0xFFFF),
        (unsigned int)((esp_random() & 0x0FFF) | 0x4000),
        (unsigned int)((esp_random() & 0x3FFF) | 0x8000),
        (unsigned int)esp_random(),
        (unsigned int)(esp_random() & 0xFFFF));
    return buf;
}

// Called by PubSubClient whenever a message arrives on a subscribed topic.
// Expects: {"event_id":..., "event_type":..., "status":"OK|CREATED|ERROR", "message":"..."}
void messageHandler(char* topic, byte* payload, unsigned int length) {
    StaticJsonDocument<256> doc;
    DeserializationError err = deserializeJson(doc, payload, length);
    if (err) {
        Serial.print("Status JSON parse failed: ");
        Serial.println(err.c_str());
        return;
    }

    StatusRecord statusMessage = {};
    strncpy(statusMessage.eventID, doc["event_id"] | "", sizeof(statusMessage.eventID) - 1);
    statusMessage.eventID[sizeof(statusMessage.eventID) - 1] = '\0';

    strncpy(statusMessage.status, doc["status"] | "UNKNOWN", sizeof(statusMessage.status) - 1);
    statusMessage.status[sizeof(statusMessage.status) - 1] = '\0';

    strncpy(statusMessage.message, doc["message"] | "", sizeof(statusMessage.message) - 1);
    statusMessage.message[sizeof(statusMessage.message) - 1] = '\0';

    Serial.printf("Status from backend: %s - %s\n", statusMessage.status, statusMessage.message);
    xQueueSend(statusQueue, &statusMessage, DISPLAY_SEND_TIMEOUT);
}

void connectAWS() {
    if (WiFi.status() != WL_CONNECTED) {
        WiFi.mode(WIFI_STA);
        WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
        Serial.print("Connecting to WiFi");
        while (WiFi.status() != WL_CONNECTED) {
            delay(500);
            Serial.print(".");
        }
        Serial.println(" connected");
    }

    net.setCACert(AWS_CERT_CA);
    net.setCertificate(AWS_CERT_CRT);
    net.setPrivateKey(AWS_CERT_PRIVATE);

    client.setBufferSize(512); // default 256 is tight for topic+JSON payload
    client.setKeepAlive(30);   // more headroom than the 15s default
    client.setServer(AWS_IOT_ENDPOINT, 8883);
    client.setCallback(messageHandler);

    Serial.print("Connecting to AWS IoT");
    uint8_t attempts = 0;
    while (!client.connect(DEVICE_ID) && attempts < 10) {
        Serial.printf(" state=%d", client.state());
        attempts++;
        delay(1000);
    }

    if (!client.connected()) {
        Serial.println(" AWS IoT connection failed!");
        stateManager(SystemState::LTEState::Disconnected);
        return;
    }

    if (client.subscribe(subTopic)) {
        Serial.printf("Subscribed to %s\n", subTopic);
        stateManager(SystemState::LTEState::Connected);
        Serial.println("AWS IoT connected!");
    }

    
}

bool publishEvent(EventRecord& rec) {
    StaticJsonDocument<256> doc;
    doc["event_id"] = rec.eventID;
    doc["event_type"] = rec.event_type;
    doc["fingerprint_id"] = rec.userID;
    doc["timestamp"] = rec.datetime_utc;

    char buffer[512];
    size_t n = serializeJson(doc, buffer, sizeof(buffer));
    (void)n;

    if (client.publish(pubTopic, buffer)) {
        Serial.print("Published: ");
        Serial.println(buffer);
        return true;
    }

    Serial.printf("Publish failed, client.state()=%d\n", client.state());
    return false;
}

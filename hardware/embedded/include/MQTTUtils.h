#pragma once
#include "Types.h"

// RFC4122-ish v4 UUID using esp_random(); good enough as a correlation id,
// not cryptographically rigorous.
char *generateEventId();

// PubSubClient callback: parses {"status":..,"message":..} from the backend
// and forwards it to displayQueue.
void messageHandler(char* topic, byte* payload, unsigned int length);

// Builds pubTopic/subTopic, connects WiFi + TLS + MQTT, subscribes.
// Safe to call again to reconnect - it early-returns the WiFi step if
// already connected.
void connectAWS();

// Serializes an EventRecord to JSON (adding a fresh event_id) and publishes
// it to pubTopic.
bool publishEvent(EventRecord &rec);

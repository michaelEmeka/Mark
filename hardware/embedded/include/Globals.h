#pragma once
#include <Arduino.h>
#include <RTClib.h>
#include <Adafruit_Fingerprint.h>
#include <HardwareSerial.h>
#include <Preferences.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <freertos/FreeRTOS.h>
#include <freertos/queue.h>

#include "Config.h"
#include "Types.h"
#include "SystemState.h"

// Peripheral / driver objects (defined in main.cpp)
extern HardwareSerial mSerial;
extern Adafruit_Fingerprint mFinger;
extern RTC_DS3231 rtc;
extern Preferences prefs;
extern Adafruit_SSD1306 display;

// MQTT / AWS IoT objects (defined in main.cpp)
extern WiFiClientSecure net;
extern PubSubClient client;
extern char pubTopic[64];
extern char subTopic[64];

// FreeRTOS queues (created in setup(), defined in main.cpp)
extern QueueHandle_t networkQueue;
extern QueueHandle_t displayQueue;

// App-level singletons (defined in main.cpp)
extern SystemState state;
extern Configs configs;
extern Nav nav;

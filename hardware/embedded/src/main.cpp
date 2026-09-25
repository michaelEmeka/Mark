#include <Arduino.h>
#include "Config.h"
#include "Types.h"
#include "SystemState.h"
#include "Globals.h"
#include "ConfigManager.h"
#include "RTCUtils.h"
#include "DisplayUtils.h"
#include "MQTTUtils.h"
#include "FingerprintUtils.h"
#include "Tasks.h"

// ---------------- Global object definitions ----------------
// (declared `extern` in Globals.h, defined once here)

HardwareSerial mSerial(2);
Adafruit_Fingerprint mFinger(&mSerial);
RTC_DS3231 rtc;
Preferences prefs;
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

WiFiClientSecure net;
PubSubClient client(net);
char pubTopic[64];
char subTopic[64];

QueueHandle_t networkQueue;
QueueHandle_t displayQueue;

SystemState state{
      SystemState::LTEState::Disconnected,
      SystemState::FGPState::Idle,
      SystemState::UPDState::Updated
    };

Configs configs;
Nav nav;

// ---------------- Setup / Loop ----------------

void setup()
{
    Wire.begin(Pins::I2C_SDA, Pins::I2C_SCL);
    Serial.begin(115200);
    mSerial.begin(57600, SERIAL_8N1, Pins::FINGER_RX, Pins::FINGER_TX);
    mFinger.begin(57600);
    nav.setup();
    configManager('R'); // reads from flash

    snprintf(pubTopic, sizeof(pubTopic), "attendance/device/%s/events", DEVICE_ID);
    snprintf(subTopic, sizeof(subTopic), "attendance/device/%s/status", DEVICE_ID);

    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C))
    {
        Serial.println("OLED init failed");
        while (1);
    }

    alertDisplay(0, 0, "..init", 1);

    if (mFinger.verifyPassword()) {
        Serial.println("Fingerprint sensor found!");
    } else {
        Serial.println("Fingerprint sensor NOT found!");
        while (1);
    }

    if (!rtc.begin()) {
      Serial.println("Couldn't find RTC");
      while (1);
    }

    DateTime local(__DATE__, __TIME__);
    DateTime utc = local - TimeSpan(3600); // Nigeria UTC+1
    rtc.adjust(utc);

    welcomeDisplay();

    networkQueue = xQueueCreate(10, sizeof(EventRecord));
    displayQueue = xQueueCreate(10, DISPLAY_MSG_LEN);

    xTaskCreate(fingerprintTask, "Fingerprint", 4096, NULL, 3, NULL);
    xTaskCreate(networkTask,     "Network",     16384, NULL, 2, NULL);
    xTaskCreate(displayTask,     "Display",     4096, NULL, 1, NULL);
}

void loop()
{
}

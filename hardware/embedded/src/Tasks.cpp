#include "Tasks.h"
#include "Globals.h"
#include "SystemState.h"
#include "FingerprintUtils.h"
#include "MQTTUtils.h"
#include "DisplayUtils.h"
#include "RTCUtils.h"

void fingerprintTask(void *parameter)
{
    while(true)
    {
        Serial.println("Fingerprint Task");
        uint8_t p, id;
        p = scanFingerprint(id);

        if (p == FINGERPRINT_OK){
          char msg[DISPLAY_MSG_LEN];
          snprintf(msg, sizeof(msg), "Processing");
          xQueueSend(displayQueue, msg, DISPLAY_SEND_TIMEOUT);

          vTaskDelay(pdMS_TO_TICKS(2000));
          snprintf(msg, sizeof(msg), "SN: %d", id);
          xQueueSend(displayQueue, msg, DISPLAY_SEND_TIMEOUT);

          if (id == ADMIN_ID)
          {
            snprintf(msg, sizeof(msg), "Enrolling..");
            xQueueSend(displayQueue, msg, DISPLAY_SEND_TIMEOUT);
            Serial.println("Enrolling..");
            enrollFingerprint();
          }
          else
          {
            // Regular match -> queue attendance event for networkTask to publish
            EventRecord rec;
            strncpy(rec.event_type, "fingerprint_scan", sizeof(rec.event_type));
            rec.userID = id;
            getCurrentDateTime().toCharArray(rec.datetime_utc, sizeof(rec.datetime_utc));
            xQueueSend(networkQueue, &rec, portMAX_DELAY);
          }
        }

        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

void networkTask(void *pvParameters){
  connectAWS();

  EventRecord rec;
  while(1){
    if (!client.connected()){
      Serial.printf("MQTT disconnected, client.state()=%d, RSSI=%d\n", client.state(), WiFi.RSSI());
      stateManager(SystemState::LTEState::Disconnected);
      connectAWS();
    }

    client.loop(); // must run frequently: keeps connection alive + delivers subscribed messages

    if (xQueueReceive(networkQueue, &rec, 0) == pdTRUE){
      publishEvent(rec);
    }

    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void displayTask(void *pvParameters){
  while(1){
    char msg[DISPLAY_MSG_LEN];

    if(xQueueReceive(displayQueue, msg, portMAX_DELAY))
    {
        Serial.print("OLED: ");
        Serial.println(msg);

        alertDisplay(0, 0, String(msg), 2);
    }
    clearDisplay();
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

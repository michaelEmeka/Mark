#include "Tasks.h"
#include "Globals.h"
#include "SystemState.h"
#include "FingerprintUtils.h"
#include "MQTTUtils.h"
#include "DisplayUtils.h"
#include "RTCUtils.h"
#include "LoggingUtils.h"

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
            int new_id_reg = enrollFingerprint();
            // Queue the enrollment event for logging, before networkTask publishes over MQTT
            if (new_id_reg != 0)
            {
              EventRecord rec;
              snprintf(rec.eventID, sizeof(rec.eventID), "%s", generateEventId());
              snprintf(rec.event_type, sizeof(rec.event_type), "%s", "fingerprint_enrolled");
              rec.userID = new_id_reg;
              getCurrentDateTime().toCharArray(rec.datetime_utc, sizeof(rec.datetime_utc));
              
              // Log event first for Eventual consistency
              xQueueSend(loggingQueue, &rec, portMAX_DELAY);
              stateManager(SystemState::FGPState::Registered);
            }
          }
          else
          {
            // Regular match -> queue attendance event for networkTask to publish
            EventRecord rec;
            snprintf(rec.eventID, sizeof(rec.eventID), "%s", generateEventId());
            snprintf(rec.event_type, sizeof(rec.event_type), "%s", "fingerprint_scan");
            rec.userID = id;
            getCurrentDateTime().toCharArray(rec.datetime_utc, sizeof(rec.datetime_utc));
            
            // Log event first for Eventual consistency
            xQueueSend(loggingQueue, &rec, portMAX_DELAY);
            stateManager(SystemState::FGPState::Idle);
          }
        }
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

void networkTask(void *pvParameters){
  connectAWS();

  EventRecord rec;
  while(1){
    char msg[DISPLAY_MSG_LEN];
    char path[64];

    if (!client.connected()){
      Serial.printf("MQTT disconnected, client.state()=%d, RSSI=%d\n", client.state(), WiFi.RSSI());
      stateManager(SystemState::LTEState::Disconnected);
      connectAWS();
    }

    client.loop(); // must run frequently: keeps connection alive + delivers subscribed messages

    if (xQueueReceive(networkQueue, &rec, 0) == pdTRUE){
      
      if (publishEvent(rec)){
        //delete event from stored logging
        snprintf(path, sizeof(path), "%s%s", eventsDir, rec.eventID);
        deleteFile(SD, path);
        snprintf(msg, sizeof(msg), "ID %d Synced!", rec.userID);
      }
      else
        snprintf(msg, sizeof(msg), "ID %d to be Synced.", rec.userID);
      
      xQueueSend(displayQueue, msg, DISPLAY_SEND_TIMEOUT);
    }

    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void displayTask(void *pvParameters){
  while(1){
    char msg[DISPLAY_MSG_LEN];

    if (xQueueReceive(displayQueue, msg, pdMS_TO_TICKS(250)) == pdTRUE)
    {
        Serial.print("OLED: ");
        Serial.println(msg);
        alertDisplay(0, 0, String(msg), 2);
    }
    else
    {
        clearDisplay();
    }

    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void loggingTask(void *pvParameters){
  EventRecord rec;
  if (!SD.exists("/attendance")) {
    createDir(SD, "/attendance");
  }

  if (!SD.exists("/attendance/events")) {
      createDir(SD, "/attendance/events");
  }

  while(1){
    char path[64];
    char msg[DISPLAY_MSG_LEN];

    if (xQueueReceive(loggingQueue, &rec, portMAX_DELAY))
    {
      snprintf(path, sizeof(path), "%s%s", eventsDir, rec.eventID);
      if (writeFile(SD, path, &rec)){
        Serial.println("Event logged");

        // Send logged event to networkQueue and status update to display queue
        snprintf(msg, sizeof(msg), "Saved ID %d", rec.userID);
        xQueueSend(networkQueue, &rec, portMAX_DELAY);
        xQueueSend(displayQueue, msg, DISPLAY_SEND_TIMEOUT);
      }
      else
      {
          // Write failed → put record back in queue
          Serial.println("Write failed, re-queuing event");
          if (xQueueSend(loggingQueue, &rec, portMAX_DELAY) != pdTRUE){
            Serial.println("Logging queue full!");
          }
      }
    }
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}
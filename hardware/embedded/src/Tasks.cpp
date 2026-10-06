#include "Tasks.h"
#include "Globals.h"
#include "SystemState.h"
#include "FingerprintUtils.h"
#include "MQTTUtils.h"
#include "DisplayUtils.h"
#include "RTCUtils.h"
#include "LoggingUtils.h"

void fingerprintTask(void* parameter) {
    while (true) {
        Serial.println("Fingerprint Task");
        uint8_t p, id;
        p = scanFingerprint(id);

        if (p == FINGERPRINT_OK) {
            char msg[DISPLAY_MSG_LEN];
            snprintf(msg, sizeof(msg), "Processing");
            xQueueSend(displayQueue, msg, DISPLAY_SEND_TIMEOUT);

            vTaskDelay(pdMS_TO_TICKS(2000));

            snprintf(msg, sizeof(msg), "SN: %d", id);
            xQueueSend(displayQueue, msg, DISPLAY_SEND_TIMEOUT);

            if (id == ADMIN_ID) {
                snprintf(msg, sizeof(msg), "Enrolling..");
                xQueueSend(displayQueue, msg, DISPLAY_SEND_TIMEOUT);
                Serial.println("Enrolling..");

                int new_id_reg = enrollFingerprint();
                // Queue the enrollment event for logging, before networkTask
                // publishes over MQTT
                if (new_id_reg != 0) {
                    EventRecord rec;
                    snprintf(rec.eventID, sizeof(rec.eventID), "%s", generateEventId());
                    snprintf(rec.event_type, sizeof(rec.event_type), "%s", "fingerprint_enrolled");
                    rec.userID = new_id_reg;
                    getCurrentDateTime(3600).toCharArray(rec.datetime_utc, sizeof(rec.datetime_utc));
                    snprintf(rec.datetime_utc, sizeof(rec.datetime_utc), "%sZ", getCurrentDateTime().c_str());

                    // Log event first for eventual consistency
                    xQueueSend(loggingQueue, &rec, portMAX_DELAY);
                    stateManager(SystemState::FGPState::Registered);
                }
            } else {
                // Regular match -> queue attendance event for networkTask to publish
                EventRecord rec;
                snprintf(rec.eventID, sizeof(rec.eventID), "%s", generateEventId());
                snprintf(rec.event_type, sizeof(rec.event_type), "%s", "fingerprint_scan");
                rec.userID = id;
                getCurrentDateTime(3600).toCharArray(rec.datetime_utc, sizeof(rec.datetime_utc));
                snprintf(rec.datetime_utc, sizeof(rec.datetime_utc), "%sZ", getCurrentDateTime().c_str());

                // Log event first for eventual consistency
                xQueueSend(loggingQueue, &rec, portMAX_DELAY);
                stateManager(SystemState::FGPState::Idle);
            }
        }

        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

void networkTask(void* pvParameters) {
    connectAWS();
    EventRecord rec;

    while (1) {
        char msg[DISPLAY_MSG_LEN];

        if (!client.connected()) {
            Serial.printf("MQTT disconnected, client.state()=%d, RSSI=%d\n", client.state(), WiFi.RSSI());
            stateManager(SystemState::LTEState::Disconnected);
            connectAWS();
        }

        client.loop(); // must run frequently: keeps connection alive + delivers subscribed messages

        if (xQueueReceive(networkQueue, &rec, 0) == pdTRUE) {
            if (publishEvent(rec)) {
                snprintf(msg, sizeof(msg), "ID %d Synced!", rec.userID);
            } else {
                snprintf(msg, sizeof(msg), "ID %d to be Synced.", rec.userID);
            }
            xQueueSend(displayQueue, msg, DISPLAY_SEND_TIMEOUT);
        }

        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

void statusTask(void* pvParameters) {
    StatusRecord statusMessage;
    Serial.println("Status Task");
    while (1) {
        if (xQueueReceive(statusQueue, &statusMessage, portMAX_DELAY) == pdTRUE) {
            char path[72];
            char msg[DISPLAY_MSG_LEN];

            snprintf(path, sizeof(path), "%s/%s", eventsDir, statusMessage.eventID);

            if (strcmp(statusMessage.status, "OK") == 0 || strcmp(statusMessage.status, "CREATED") == 0 || strcmp(statusMessage.status, "ERROR") == 0) {
                deleteFile(SD, path);
                vTaskDelay(pdMS_TO_TICKS(100)); // Allow time for the filesystem to update
            }

            snprintf(msg, sizeof(msg), "%s: %s", statusMessage.status, statusMessage.message);
            xQueueSend(displayQueue, msg, DISPLAY_SEND_TIMEOUT);
        }
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

void displayTask(void* pvParameters) {
    while (1) {
        char msg[DISPLAY_MSG_LEN];

        if (xQueueReceive(displayQueue, msg, pdMS_TO_TICKS(250)) == pdTRUE) {
            Serial.print("OLED: ");
            Serial.println(msg);
            alertDisplay(msg);
        } else {
            clearDisplay();
        }

        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

void loggingTask(void* pvParameters) {
    EventRecord rec;

    if (!SD.exists("/attendance")) {
        createDir(SD, "/attendance");
    }

    if (!SD.exists("/attendance/events")) {
        createDir(SD, "/attendance/events");
    }

    while (1) {
        char path[72];
        char msg[DISPLAY_MSG_LEN];

        if (xQueueReceive(loggingQueue, &rec, portMAX_DELAY)) {
            snprintf(path, sizeof(path), "%s/%s", eventsDir, rec.eventID);
            if (writeFile(SD, path, &rec)) {
                Serial.println("Event logged");

                // Send logged event to networkQueue and status update to display queue
                snprintf(msg, sizeof(msg), "Saved ID %d", rec.userID);
                xQueueSend(networkQueue, &rec, portMAX_DELAY);
                xQueueSend(displayQueue, msg, DISPLAY_SEND_TIMEOUT);
            } else {
                // Write failed - put record back in queue
                Serial.println("Write failed, re-queuing event");
                if (xQueueSend(loggingQueue, &rec, portMAX_DELAY) != pdTRUE) {
                    Serial.println("Logging queue full!");
                }
            }
        }

        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

void retryTask(void* pvParameters) {
    // const TickType_t retryInterval = pdMS_TO_TICKS(30000);
    const TickType_t retryInterval = pdMS_TO_TICKS(5000);

    /////////
    //////// WE WANT TO CHECK EACH RETRIED FILE TRANSMIT FIRST IF IT STILL EXISTS ON THE SD CARD
    ////// BEFORE ATTEMPTING TO SEND ANOTHER EVENT TO THE NETWORK QUEUE. OTHERWISE, WE RISK FILLING THE NETWORK QUEUE WITH DUPLICATE EVENTS.
    ///////// A SOLUTION IS TO CHECK IF THE FILE STILL EXISTS ON THE SD CARD BEFORE ATTEMPTING TO SEND IT TO THE NETWORK QUEUE. IF IT DOESN'T EXIST, IT HAS BEEN ACKNOWLEDGED AND DELETED BY STATUS TASK, WE CAN SKIP IT AND MOVE ON TO THE NEXT FILE.
    ///////// PROBABLY USING AN ACK QUEUE from STATUS to RETRY task
    
    while (1) {
        vTaskDelay(retryInterval);
        Serial.println("Retry Task");

        if (state.LTE != SystemState::LTEState::Connected) {
            Serial.println("LTE not connected, skipping retry");
            continue;
        }

        if (!SD.exists(eventsDir)) {
            Serial.println("eventsDir does not exist, skipping retry");
            continue;
        }

        File dir = SD.open(eventsDir);
        if (!dir || !dir.isDirectory()) {
            if (dir) {
                dir.close();
            }
            continue;
        }

        while (File entry = dir.openNextFile()) {
            if (!entry.isDirectory()) {
                char path[72];
                snprintf(path, sizeof(path), "%s/%s", eventsDir, entry.name());

                EventRecord rec = readFile(SD, path);
                if (strlen(rec.eventID) == 0) {
                    Serial.printf("Skipping unreadable event file: %s\n", path);
                    if (deleteFile(SD, path)) {
                        Serial.printf("Deleted unreadable event file: %s\n", path);
                    }
                    entry.close();
                    continue;
                }

                if (xQueueSend(networkQueue, &rec, 0) == pdTRUE) {
                    Serial.printf("Queued retry for SD-backed event %s\n", rec.eventID);
                } else {
                    Serial.println("Network queue full; will retry on next pass");
                }
            }

            entry.close();
        }

        dir.close();
    }
}

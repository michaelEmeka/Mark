#include "FingerprintUtils.h"
#include "Globals.h"
#include "SystemState.h"
#include "ConfigManager.h"
#include "RTCUtils.h"

bool idSelector(uint8_t &current_id)
{
  if (!digitalRead(nav.leftButton) && (current_id > 0))
  {
    current_id--;
    Serial.print("Waiting for valid mFinger to enroll as #");
    Serial.println(current_id);
    vTaskDelay(pdMS_TO_TICKS(500));
  }
  else if (!digitalRead(nav.rightButton) && (current_id < 127))
  {
    current_id++;
    Serial.print("Waiting for valid mFinger to enroll as #");
    Serial.println(current_id);
    vTaskDelay(pdMS_TO_TICKS(500));
  }
  return true;
}

uint8_t scanFingerprint(uint8_t &id)
{
  Serial.println("Scan to Mark Attendance");
  stateManager(SystemState::FGPState::Scanning);

  uint8_t p = mFinger.getImage();

  if (p != FINGERPRINT_OK)
    return p;

  p = mFinger.image2Tz();
  if (p != FINGERPRINT_OK)
    return p;

  p = mFinger.fingerFastSearch();

  switch (p)
  {
  case (FINGERPRINT_OK):
    stateManager(SystemState::FGPState::Identified);
    Serial.print("Found ID #");
    id = mFinger.fingerID;
    Serial.print(id);
    Serial.print(" with confidence ");
    Serial.println(mFinger.confidence);
    break;
  case (FINGERPRINT_NOTFOUND):
    Serial.println("No match found");
    break;
  default:
    Serial.println("Search Error");
    break;
  }
  return p;
}


uint8_t enrollFingerprint()
{
    int p = -1;
    uint8_t new_id_reg = configs.last_id_reg + 1;

    stateManager(SystemState::FGPState::Scanning);

    // --------------------------------------------------
    // FIRST SCAN
    // --------------------------------------------------
    while (p != FINGERPRINT_OK && idSelector(new_id_reg))
    {
        Serial.print("Waiting for valid mFinger to enroll as #");
        Serial.println(new_id_reg);

        //Display currently enrolled id from selector
        char msg[DISPLAY_MSG_LEN];
        snprintf(msg, sizeof(msg), "Enrolling.. ID %d", new_id_reg);
        xQueueSend(displayQueue, msg, DISPLAY_SEND_TIMEOUT);

        p = mFinger.getImage();

        switch (p)
        {
        case FINGERPRINT_OK:
            Serial.println("Image taken");
            break;

        case FINGERPRINT_NOFINGER:
            Serial.print(".");
            break;

        case FINGERPRINT_PACKETRECIEVEERR:
            Serial.println("Communication error");
            return 0;

        case FINGERPRINT_IMAGEFAIL:
            Serial.println("Imaging error");
            return 0;

        default:
            Serial.println("Unknown error");
            return 0;
        }
    }

    // If the loop ended because idSelector() failed
    // rather than because a fingerprint was captured.
    if (p != FINGERPRINT_OK)
    {
        Serial.println("Could not select a valid fingerprint ID");
        return 0;
    }

    // --------------------------------------------------
    // CONVERT FIRST IMAGE
    // --------------------------------------------------
    p = mFinger.image2Tz(1);

    switch (p)
    {
    case FINGERPRINT_OK:
        Serial.println("Image converted");
        break;

    case FINGERPRINT_IMAGEMESS:
        Serial.println("Image too messy");
        return 0;

    case FINGERPRINT_PACKETRECIEVEERR:
        Serial.println("Communication error");
        return 0;

    case FINGERPRINT_INVALIDIMAGE:
        Serial.println("Invalid image");
        return 0;

    default:
        Serial.println("Unknown error");
        return 0;
    }

    // --------------------------------------------------
    // REMOVE FINGER
    // --------------------------------------------------
    Serial.println("Remove mFinger");

    vTaskDelay(pdMS_TO_TICKS(2000));

    p = 0;

    while (p != FINGERPRINT_NOFINGER)
    {
        p = mFinger.getImage();

        if (p == FINGERPRINT_PACKETRECIEVEERR)
        {
            Serial.println("Communication error");
            return 0;
        }

        if (p == FINGERPRINT_IMAGEFAIL)
        {
            Serial.println("Imaging error");
            return 0;
        }
    }

    Serial.print("ID ");
    Serial.println(new_id_reg);

    // --------------------------------------------------
    // SECOND SCAN
    // --------------------------------------------------
    p = -1;

    Serial.println("Place same mFinger again");

    while (p != FINGERPRINT_OK)
    {
        p = mFinger.getImage();

        switch (p)
        {
        case FINGERPRINT_OK:
            Serial.println("Image taken");
            break;

        case FINGERPRINT_NOFINGER:
            Serial.print(".");
            break;

        case FINGERPRINT_PACKETRECIEVEERR:
            Serial.println("Communication error");
            return 0;

        case FINGERPRINT_IMAGEFAIL:
            Serial.println("Imaging error");
            return 0;

        default:
            Serial.println("Unknown error");
            return 0;
        }
    }

    // --------------------------------------------------
    // CONVERT SECOND IMAGE
    // --------------------------------------------------
    p = mFinger.image2Tz(2);

    switch (p)
    {
    case FINGERPRINT_OK:
        Serial.println("Image converted");
        break;

    case FINGERPRINT_IMAGEMESS:
        Serial.println("Image too messy");
        return 0;

    case FINGERPRINT_PACKETRECIEVEERR:
        Serial.println("Communication error");
        return 0;

    case FINGERPRINT_INVALIDIMAGE:
        Serial.println("Invalid image");
        return 0;

    default:
        Serial.println("Unknown error");
        return 0;
    }

    // --------------------------------------------------
    // CREATE MODEL
    // --------------------------------------------------
    Serial.print("Creating model for #");
    Serial.println(new_id_reg);

    p = mFinger.createModel();

    switch (p)
    {
    case FINGERPRINT_OK:
        Serial.println("Prints matched!");
        break;

    case FINGERPRINT_PACKETRECIEVEERR:
        Serial.println("Communication error");
        return 0;

    case FINGERPRINT_ENROLLMISMATCH:
        Serial.println("Fingerprints did not match");
        return 0;

    default:
        Serial.println("Unknown error");
        return 0;
    }

    // --------------------------------------------------
    // STORE MODEL
    // --------------------------------------------------
    Serial.print("ID ");
    Serial.println(new_id_reg);

    p = mFinger.storeModel(new_id_reg);

    switch (p)
    {
    case FINGERPRINT_OK:
        Serial.println("Stored!");
        break;

    case FINGERPRINT_PACKETRECIEVEERR:
        Serial.println("Communication error");
        return 0;

    case FINGERPRINT_BADLOCATION:
        Serial.println("Could not store in that location");
        return 0;

    case FINGERPRINT_FLASHERR:
        Serial.println("Error writing to flash");
        return 0;

    default:
        Serial.println("Unknown error");
        return 0;
    }

    // --------------------------------------------------
    // ENROLLMENT SUCCESS
    // --------------------------------------------------
    configs.last_id_reg = new_id_reg;
    configManager('W');

    return new_id_reg;
}
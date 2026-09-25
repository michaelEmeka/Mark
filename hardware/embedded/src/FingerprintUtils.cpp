#include "FingerprintUtils.h"
#include "Globals.h"
#include "SystemState.h"
#include "ConfigManager.h"
#include "RTCUtils.h"

bool idSelector(uint8_t &current_id){
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

uint8_t scanFingerprint(uint8_t &id){
  Serial.println("Scan to Mark Attendance");
  stateManager(SystemState::FGPState::Scanning);

  uint8_t p = mFinger.getImage();

  if (p != FINGERPRINT_OK)
    return p;

  p = mFinger.image2Tz();
  if (p != FINGERPRINT_OK)
    return p;

  p = mFinger.fingerFastSearch();

  switch(p){
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

uint8_t enrollFingerprint(){
  int p = -1;
  uint8_t new_id_reg = configs.last_id_reg + 1;

  stateManager(SystemState::FGPState::Scanning);

  while (p != FINGERPRINT_OK && (idSelector(new_id_reg))) {

    Serial.print("Waiting for valid mFinger to enroll as #");
    Serial.println(new_id_reg);

    p = mFinger.getImage();
    switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      Serial.print(".");
      break;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      break;
    case FINGERPRINT_IMAGEFAIL:
      Serial.println("Imaging error");
      break;
    default:
      Serial.println("Unknown error");
      break;
    }
  }

  // OK success!
  p = mFinger.image2Tz(1);
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  Serial.println("Remove mFinger");
  delay(2000);
  p = 0;
  while (p != FINGERPRINT_NOFINGER) {
    p = mFinger.getImage();
  }
  Serial.print("ID "); Serial.println(new_id_reg);
  p = -1;
  Serial.println("Place same mFinger again");
  while (p != FINGERPRINT_OK) {
    p = mFinger.getImage();
    switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      Serial.print(".");
      break;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      break;
    case FINGERPRINT_IMAGEFAIL:
      Serial.println("Imaging error");
      break;
    default:
      Serial.println("Unknown error");
      break;
    }
  }

  // OK success!
  p = mFinger.image2Tz(2);
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  // OK converted!
  Serial.print("Creating model for #"); Serial.println(new_id_reg);

  p = mFinger.createModel();
  if (p == FINGERPRINT_OK) {
    Serial.println("Prints matched!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_ENROLLMISMATCH) {
    Serial.println("Fingerprints did not match");
    return p;
  } else {
    Serial.println("Unknown error");
    return p;
  }

  // store fingerprint with id
  Serial.print("ID "); Serial.println(new_id_reg);
  p = mFinger.storeModel(new_id_reg);
  if (p == FINGERPRINT_OK) {
    stateManager(SystemState::FGPState::Registered);

    Serial.println("Stored!");
    configs.last_id_reg = new_id_reg;
    configManager('W');

    // Queue the enrollment event for networkTask to publish over MQTT
    EventRecord rec;
    strncpy(rec.event_type, "fingerprint_enrolled", sizeof(rec.event_type));
    rec.userID = new_id_reg;
    getCurrentDateTime().toCharArray(rec.datetime_utc, sizeof(rec.datetime_utc));
    xQueueSend(networkQueue, &rec, portMAX_DELAY);
  }
  else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("Communication error");
    return p;
  }
  else if (p == FINGERPRINT_BADLOCATION) {
    Serial.println("Could not store in that location");
    return p;
  }
  else if (p == FINGERPRINT_FLASHERR) {
    Serial.println("Error writing to flash");
    return p;
  }
  else {
    Serial.println("Unknown error");
    return p;
  }

  return true;
}

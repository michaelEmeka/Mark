#pragma once
#include <Arduino.h>
#include "Config.h"

typedef struct EventRecord {
    char eventID[40];
    char event_type[32]; // "fingerprint_enrolled" or "fingerprint_scan"
    int userID;
    char datetime_utc[32];
} EventRecord;

typedef struct Configs {
  uint8_t last_id_reg = 1;
  uint8_t admin_id;
  uint8_t device_id;
} Configs;

typedef struct Nav {
  const uint8_t leftButton = Pins::NAV_LEFT;
  const uint8_t rightButton = Pins::NAV_RIGHT;
  void setup(){
    pinMode(leftButton, INPUT_PULLUP);
    pinMode(rightButton, INPUT_PULLUP);
  }
} Nav;

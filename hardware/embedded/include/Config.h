#pragma once
#include <Arduino.h>

// ---- OLED ----
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

// ---- Identity ----
constexpr uint8_t ADMIN_ID = 1;
constexpr const char* DEVICE_ID = "FUTO_SESET_ELE_01";

// ---- FreeRTOS queue behaviour ----
// How long any task will wait for a slot in displayQueue before giving up.
// Kept short and non-blocking-forever so a backed-up display can never stall
// networkTask (which would stop client.loop() and drop the MQTT keepalive).
#define DISPLAY_SEND_TIMEOUT pdMS_TO_TICKS(50)

// Fixed-size buffer for display messages. IMPORTANT: never put Arduino String
// through a FreeRTOS queue - xQueueSend/Receive memcpy raw bytes without
// calling String's copy constructor/destructor, so the sender's dtor frees
// the heap buffer the receiver's copy still points to (use-after-free, then
// a double free when the receiver's own copy is destructed). That's what was
// causing the heap corruption crashes. Plain char arrays are safe to memcpy.
#define DISPLAY_MSG_LEN 48

// ---- Pin map ----
namespace Pins {
  constexpr uint8_t FINGER_RX = 16;
  constexpr uint8_t FINGER_TX = 17;
  constexpr uint8_t I2C_SDA   = 21;
  constexpr uint8_t I2C_SCL   = 22;
  constexpr uint8_t NAV_LEFT  = 32;
  constexpr uint8_t NAV_RIGHT = 33;
}

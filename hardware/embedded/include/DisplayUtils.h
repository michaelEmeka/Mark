#pragma once
#include <Arduino.h>

// Centers `text` on the OLED at the given size and draws it.
void alertDisplay(uint8_t x = 0, uint8_t y = 0, String text = "", uint8_t size = 0);

// Blocks 1s then clears the OLED (called between displayTask messages).
void clearDisplay();

// Plays the boot-up "Hi / I'm Mark" splash sequence.
void welcomeDisplay();

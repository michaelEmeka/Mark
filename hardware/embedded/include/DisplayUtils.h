#pragma once

#include <Arduino.h>

// Centers `text` on the OLED and draws it.
void alertDisplay(const char* text);

// Clears the OLED (used between displayTask messages).
void clearDisplay();

// Plays the boot-up "Hi / I'm Mark" splash sequence.
void welcomeDisplay();
#include "main.h"
#include "oled.h"

OLED oled;

void setup() {
    Wire.begin();
    Serial.begin(115200);
    if (!oled.begin()) {
        Serial.println("OLED init failed");
        while (true) { delay(1000); }
    }
    Serial.println("OLED init successful");
}

void loop() {
    oled.displayText("Hello", 1, 1, 2);
    Serial.println("Hello displayed");
    delay(2000);
    oled.clearDisplay();
    Serial.println("Display cleared");
    delay(2000);
}
#ifndef OLED_H
#define OLED_H

#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Wire.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

class OLED {
private:
    Adafruit_SSD1306 display;
public:
    OLED()
        : display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1){}// Wire hasn't been initialized yet

    bool begin()
    {
        if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
            return false;
        }
        display.clearDisplay();
        display.display();
        return true;
    }

    void displayText(const String &text, int x, int y, int size)
    {
        display.clearDisplay();
        display.setCursor(x, y);
        display.setTextSize(size);
        display.setTextColor(SSD1306_WHITE);
        display.println(text);
        display.display();
    }

    void clearDisplay(){
        display.clearDisplay();
        display.display();
    }

    //void displayUI(const String &text)
};

#endif
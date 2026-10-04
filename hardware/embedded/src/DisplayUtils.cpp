#include "DisplayUtils.h"
#include "Globals.h"

void alertDisplay(const char* text) {
    int16_t x1, y1;
    uint16_t w, h;

    display.clearDisplay();
    display.setTextColor(SSD1306_WHITE);

    float bestSize = 1.0;

    // Find the best text size that fits the screen
    for (uint8_t size = 1; size <= 4; size++) {
        display.setTextSize(size);
        display.getTextBounds(text, 0, 0, &x1, &y1, &w, &h);

        float scaleFactor = 0.8;

        if (w <= (SCREEN_WIDTH * scaleFactor) && h <= (SCREEN_HEIGHT * scaleFactor)) {
            bestSize = size;
        } else {
            break;
        }
    }

    // Apply the best size that fits
    display.setTextSize(bestSize);
    display.getTextBounds(text, 0, 0, &x1, &y1, &w, &h);

    int16_t x = ((int16_t)SCREEN_WIDTH - (int16_t)w) / 2;
    int16_t y = ((int16_t)SCREEN_HEIGHT - (int16_t)h) / 2;

    display.setCursor(x, y);
    display.print(text);
    display.display();
}

void clearDisplay() {
    display.clearDisplay();
    display.display();
}

void welcomeDisplay() {
    int n = 2;
    const char* texts[2] = {"Hi", "I'm Mark"};
    int timelines[2] = {2000, 3000};
    int sizes[2] = {3, 2};

    for (int i = 0; i < n; i++) {
        alertDisplay(texts[i]);
        vTaskDelay(pdMS_TO_TICKS(timelines[i]));
    }
}
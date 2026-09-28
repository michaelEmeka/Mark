#include "DisplayUtils.h"
#include "Globals.h"

void alertDisplay(uint8_t x, uint8_t y, String text, uint8_t size)
{
  int16_t x1, y1;
  uint16_t w, h;

  display.clearDisplay();
  display.setTextSize(size);
  display.setTextColor(SSD1306_WHITE);

  display.getTextBounds(text, 0, 0, &x1, &y1, &w, &h);

  x = (SCREEN_WIDTH - w) / 2;
  y = (SCREEN_HEIGHT - h) / 2;

  display.setCursor(x, y);
  display.print(text);
  display.display();
}

void clearDisplay(){
  display.clearDisplay();
  display.display();
}

void welcomeDisplay(){
  int n = 2;
  String texts[2] = {"Hi", "I'm Mark"};
  int timelines[2] = {2000, 3000};
  int sizes[2] = {3, 2};
  for (int i = 0; i < n; i++){
    alertDisplay(0, 0, texts[i], sizes[i]);
    vTaskDelay(pdMS_TO_TICKS(timelines[i]));
  }
}

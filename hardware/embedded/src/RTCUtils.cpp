#include "RTCUtils.h"
#include "Globals.h"

String getCurrentDateTime(int timespan) {
  DateTime now = rtc.now();
  DateTime adjusted = now + TimeSpan(timespan);

  char buffer[25];
  snprintf(
    buffer,
    sizeof(buffer),
    "%04d-%02d-%02dT%02d:%02d:%02dZ",
    adjusted.year(),
    adjusted.month(),
    adjusted.day(),
    adjusted.hour(),
    adjusted.minute(),
    adjusted.second()
  );

  return String(buffer);
}

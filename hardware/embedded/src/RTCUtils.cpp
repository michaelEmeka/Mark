#include "RTCUtils.h"
#include "Globals.h"

String getCurrentDateTime(int timespan){
  DateTime utc_now = rtc.now();
  DateTime converted_time = utc_now + TimeSpan(timespan); // default utc timespan=0
  return converted_time.timestamp();
}

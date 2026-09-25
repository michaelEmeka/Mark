#pragma once
#include <Arduino.h>

// Returns the current RTC time as an ISO-8601 timestamp string.
// timespan is added to the RTC's stored UTC time before formatting
// (e.g. pass a TimeSpan-compatible offset in seconds; default 0 = UTC).
String getCurrentDateTime(int timespan = 0);

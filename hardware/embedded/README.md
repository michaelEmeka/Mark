# Mark — Fingerprint Attendance Node (PlatformIO)

Split out of the single `main.cpp` into a standard PlatformIO layout:

```
include/
  Config.h          pin map + compile-time constants (screen size, admin id, queue timeouts)
  Types.h           EventRecord / Configs / Nav structs
  SystemState.h     LTE/FGP/UPD state enums + stateManager() declarations
  Globals.h         extern declarations for every shared object (single include for the "wiring")
  ConfigManager.h   flash (Preferences) read/write of Configs
  RTCUtils.h        getCurrentDateTime()
  DisplayUtils.h    OLED helpers (alertDisplay/clearDisplay/welcomeDisplay)
  MQTTUtils.h       WiFi + AWS IoT (TLS/MQTT) connect, publish, subscribe callback
  FingerprintUtils.h  scan / enroll / idSelector
  Tasks.h           the three FreeRTOS task entry points
  secrets.h.example  copy to secrets.h and fill in (gitignored)

src/
  main.cpp          defines the shared objects declared in Globals.h, setup(), loop()
  SystemState.cpp
  ConfigManager.cpp
  RTCUtils.cpp
  DisplayUtils.cpp
  MQTTUtils.cpp
  FingerprintUtils.cpp
  Tasks.cpp

platformio.ini      board=esp32dev, lib_deps for RTClib/Fingerprint/GFX/SSD1306/PubSubClient/ArduinoJson
```

## Getting it building

1. `cp include/secrets.h.example include/secrets.h` and fill in your WiFi
   credentials and AWS IoT endpoint/certs.
2. `pio run` (or the PlatformIO VS Code extension) to build.
3. `pio run -t upload -t monitor` to flash + open the serial monitor.

## Why split this way

- **`Globals.h`** is the one place that declares every object shared across
  files (`extern`), so no `.cpp` file needs to guess at ownership. All the
  actual object *definitions* live in `main.cpp` — the only file that should
  ever define them, to avoid multiple-definition link errors.
- **`Types.h` / `SystemState.h`** hold the plain data — safe to include
  anywhere with no risk of circular deps, since they don't reach into
  `Globals.h` themselves (except `SystemState.cpp`, which needs `state` and
  `displayQueue` to implement `stateManager()`).
- Each hardware concern (RTC, display, fingerprint, MQTT) gets its own
  header + source pair, mirroring the section comments already in your
  original file (`//RTC Utils`, `//Fingerprint Utils`, etc.) — I didn't
  reorganize the logic, just gave each block a home.
- **`Tasks.cpp`** is deliberately last in the include chain since it's the
  only file that touches all four modules at once.

## Two small bugs fixed in the split (flagged, not silently changed)

- `toString(SystemState::FGPState)` didn't have a case for `Idle` (falls
  through to `"Unknown"`). Added it — harmless today since `stateManager`
  only fires on a state *change* and nothing ever transitions back to
  `Idle`, but worth having if that ever changes.
- `welcomeDisplay()` declared `n = 3` but only initialized 2 entries in each
  `texts[3]`/`timelines[3]`/`sizes[3]` array — the loop's 3rd iteration was
  reading uninitialized stack memory. Fixed the arrays and `n` to both be 2,
  matching the actual "Hi" / "I'm Mark" sequence.

#pragma once

// Config manager: Reads ('R', read_only) or Writes ('W') the Configs struct
// to/from flash (Preferences/NVS).
// Workflow: read/write directly to/from the global `configs` struct;
// configManager persists it to flash and (via 'R') restores it on startup.
void configManager(char method);

#pragma once
#include <Arduino.h>

// Lets the admin nudge the candidate enrollment id up/down with the nav
// buttons while waiting for a finger. Always returns true (kept as the
// while-loop condition in enrollFingerprint).
bool idSelector(uint8_t &current_id);

// Scans a finger and searches it against the stored library. On a match,
// writes the matched id into `id` and returns FINGERPRINT_OK.
uint8_t scanFingerprint(uint8_t &id);

// Runs the two-image enroll dance for a new fingerprint, stores it at
// last_id_reg+1, persists that counter to flash, and queues a
// "fingerprint_enrolled" event for networkTask.
uint8_t enrollFingerprint();

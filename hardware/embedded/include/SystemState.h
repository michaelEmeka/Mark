#pragma once

struct SystemState {
  enum class LTEState {
      Connected,
      Disconnected
  };

  enum class FGPState {
      Idle,
      Scanning,
      Identified,
      Uploaded,
      Registered
  };

  enum class UPDState {
      Updating,
      Updated
  };

  LTEState LTE;
  FGPState FGP;
  UPDState UPD;
};

// Enum -> String converters
const char* toString(SystemState::LTEState state);
const char* toString(SystemState::FGPState state);
const char* toString(SystemState::UPDState state);

// State manager: updates the relevant sub-state if it changed, and pushes
// the new state name onto displayQueue for displayTask to render.
void stateManager(SystemState::FGPState newState);
void stateManager(SystemState::LTEState newState);
void stateManager(SystemState::UPDState newState);

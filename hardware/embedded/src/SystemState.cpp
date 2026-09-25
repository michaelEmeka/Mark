#include "SystemState.h"
#include "Globals.h"

const char* toString(SystemState::LTEState state)
{
    switch (state)
    {
        case SystemState::LTEState::Connected:    return "Connected";
        case SystemState::LTEState::Disconnected: return "Disconnected";
    }
    return "Unknown";
}

const char* toString(SystemState::FGPState state)
{
    switch (state)
    {
        case SystemState::FGPState::Idle:       return "Idle";
        case SystemState::FGPState::Scanning:   return "Scanning";
        case SystemState::FGPState::Identified: return "Identified";
        case SystemState::FGPState::Uploaded:   return "Uploaded";
        case SystemState::FGPState::Registered: return "Registered";
    }
    return "Unknown";
}

const char* toString(SystemState::UPDState state)
{
    switch (state)
    {
        case SystemState::UPDState::Updating: return "Updating";
        case SystemState::UPDState::Updated:  return "Updated";
    }
    return "Unknown";
}

void stateManager(SystemState::FGPState newState){
  if (state.FGP != newState)
  {
    state.FGP = newState;
    char msg[DISPLAY_MSG_LEN];
    snprintf(msg, sizeof(msg), "%s", toString(newState));
    xQueueSend(displayQueue, msg, DISPLAY_SEND_TIMEOUT);
  }
}

void stateManager(SystemState::LTEState newState){
  if (state.LTE != newState)
  {
    //Serial.print(toString(state.LTE));
    //Serial.println(toString(newState));
    state.LTE = newState;
    char msg[DISPLAY_MSG_LEN];
    snprintf(msg, sizeof(msg), "%s", toString(newState));
    xQueueSend(displayQueue, msg, DISPLAY_SEND_TIMEOUT);
  }
}

void stateManager(SystemState::UPDState newState){
  if (state.UPD != newState)
  {
    state.UPD = newState;
    char msg[DISPLAY_MSG_LEN];
    snprintf(msg, sizeof(msg), "%s", toString(newState));
    xQueueSend(displayQueue, msg, DISPLAY_SEND_TIMEOUT);
  }
}

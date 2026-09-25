#include "ConfigManager.h"
#include "Globals.h"

void configManager(char method){
  switch(method){
    case 'W':
      prefs.begin("config", false);
      prefs.putInt("last_id_reg", configs.last_id_reg);
      break;
    case 'R':
      prefs.begin("config", true);
      configs.last_id_reg = prefs.getInt("last_id_reg", 1);
      break;
  }
  prefs.end();
}

#include "LoggingUtils.h"
#include "Globals.h"

namespace {
    String serializeEventRecord(const EventRecord &rec) {
        return String(rec.eventID) + "," +
            String(rec.event_type) + "," +
            String(rec.userID) + "," +
            String(rec.datetime_utc) + "\n";
    }

    EventRecord parseEventRecord(const String &line) {
        EventRecord rec = {};

        int firstComma = line.indexOf(',');
        int secondComma = line.indexOf(',', firstComma + 1);
        int thirdComma = line.indexOf(',', secondComma + 1);

        if (firstComma < 0 || secondComma < 0 || thirdComma < 0) {
            return rec;
        }

        String eventID = line.substring(0, firstComma);
        String eventType = line.substring(firstComma + 1, secondComma);
        String userIDString = line.substring(secondComma + 1, thirdComma);
        String dateTime = line.substring(thirdComma + 1);
        dateTime.trim();

        eventID.toCharArray(rec.eventID, sizeof(rec.eventID));
        eventType.toCharArray(rec.event_type, sizeof(rec.event_type));
        rec.userID = userIDString.toInt();
        dateTime.toCharArray(rec.datetime_utc, sizeof(rec.datetime_utc));

        return rec;
    }
}  // namespace

EventRecord readFile(fs::FS &fs, const char *path) {
    EventRecord rec = {};

    Serial.printf("Reading file: %s\n", path);

    xSemaphoreTake(sdMutex, portMAX_DELAY);
    File file = fs.open(path, FILE_READ);
    if (!file) {
        Serial.println("Failed to open file for reading");
        xSemaphoreGive(sdMutex);
        return rec;
    }

    String line = file.readStringUntil('\n');
    file.close();
    xSemaphoreGive(sdMutex);

    if (line.length() == 0) {
        Serial.println("Event record is empty");
        return rec;
    }

    Serial.print("Read from file: ");
    Serial.println(line);

    return parseEventRecord(line);
}

bool writeFile(fs::FS &fs, const char *path, const EventRecord *rec) {
  Serial.printf("Writing file: %s\n", path);

  if (rec == nullptr) {
    Serial.println("Null EventRecord pointer");
    return false;
  }

  String line = serializeEventRecord(*rec);

  xSemaphoreTake(sdMutex, portMAX_DELAY);
  File file = fs.open(path, FILE_WRITE);
  if (!file) {
    Serial.println("Failed to open file for writing");
    xSemaphoreGive(sdMutex);
    return false;
  }

  bool written = file.print(line) > 0;
  file.close();
  xSemaphoreGive(sdMutex);

  if (written) {
    Serial.println("File written");
  } else {
    Serial.println("Write failed");
  }

  return written;
}

bool deleteFile(fs::FS &fs, const char *path) {
  Serial.printf("Deleting file: %s\n", path);
  xSemaphoreTake(sdMutex, portMAX_DELAY);
  bool ok = fs.remove(path);
  xSemaphoreGive(sdMutex);

  if (ok) {
    Serial.println("File deleted");
    return true;
  } else {
    Serial.println("Delete failed");
    return false;
  }
}

void appendFile(fs::FS &fs, const char *path, const char *message) {
  Serial.printf("Appending to file: %s\n", path);

  xSemaphoreTake(sdMutex, portMAX_DELAY);
  File file = fs.open(path, FILE_APPEND);
  if (!file) {
    Serial.println("Failed to open file for appending");
    xSemaphoreGive(sdMutex);
    return;
  }
  if (file.print(message)) {
    Serial.println("Message appended");
  } else {
    Serial.println("Append failed");
  }
  file.close();
  xSemaphoreGive(sdMutex);
}

void renameFile(fs::FS &fs, const char *path1, const char *path2) {
  Serial.printf("Renaming file %s to %s\n", path1, path2);
  
  xSemaphoreTake(sdMutex, portMAX_DELAY);
  if (fs.rename(path1, path2)) {
    Serial.println("File renamed");
  } else {
    Serial.println("Rename failed");
  }
  xSemaphoreGive(sdMutex);
}

void createDir(fs::FS &fs, const char *path) {
  Serial.printf("Creating Dir: %s\n", path);
  xSemaphoreTake(sdMutex, portMAX_DELAY);
  if (fs.mkdir(path)) {
    Serial.println("Dir created");
  } else {
    Serial.println("mkdir failed");
  }
  xSemaphoreGive(sdMutex);
}
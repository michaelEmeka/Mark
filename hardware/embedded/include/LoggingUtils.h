#pragma once
#include <Arduino.h>
#include <FS.h>
#include <SD.h>
#include <SPI.h>

#include "Types.h"

EventRecord readFile(fs::FS &fs, const char *path);
bool writeFile(fs::FS &fs, const char *path, const EventRecord *rec);
bool deleteFile(fs::FS &fs, const char* path);
void appendFile(fs::FS, const char*, const char*);
void renameFile(fs::FS, const char*, const char*);
void createDir(fs::FS &fs, const char *path);
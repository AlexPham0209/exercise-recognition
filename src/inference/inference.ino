/* Copyright 2020 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#include <TensorFlowLite.h>

#include "main_functions.h"

#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "constants.h"
#include "model.h"
#include "output_handler.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "tensorflow/lite/version.h"
#include <Arduino_LSM9DS1.h>

const float accelerationThreshold = 2.5; // threshold of significant in G's
const int numSamples = 119;

int samplesRead = numSamples;

float max_val = -10000;
float min_val = 10000;

void printData(float aX, float aY, float aZ, float gX, float gY, float gZ) {
  //print the data in CSV format
    Serial.print(aX, 3);
    Serial.print(',');
    Serial.print(aY, 3);
    Serial.print(',');
    Serial.print(aZ, 3);
    Serial.print(',');
    Serial.print(gX, 3);
    Serial.print(',');
    Serial.print(gY, 3);
    Serial.print(',');
    Serial.print(gZ, 3);
    Serial.println();
} 
void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  // print the header
  Serial.println("aX,aY,aZ,gX,gY,gZ");
}

void loop() {
  float aX, aY, aZ, gX, gY, gZ;

  // check if the all the required samples have been read since
  // the last time the significant motion was detected
  for (int i = 0; i < numSamples; ++i) {
    // check if both new acceleration and gyroscope data is
    // available
    if (!IMU.accelerationAvailable() || !IMU.gyroscopeAvailable())
      break;

    // read the acceleration and gyroscope data
    // Accelerometer data between [-4, 4]
    // Gyroscopic data between [-2000, 2000] 
    IMU.readAcceleration(aX, aY, aZ);
    IMU.readGyroscope(gX, gY, gZ);

    // Normalizing data between [-1, 1]
    aX /= 4;
    aY /= 4;
    aZ /= 4;

    gX /= 2000;
    gY /= 2000;
    gZ /= 2000;

    printData(aX, aY, aZ, gX, gY, gZ);
  }

  Serial.println();
}

/* Copyright 2023 The TensorFlow Authors. All Rights Reserved.

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

#include "constants.h"
#include "main_functions.h"
#include "model.h"
#include "output_handler.h"
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_log.h"
#include "tensorflow/lite/micro/system_setup.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include <Arduino_LSM9DS1.h>

const float accelerationThreshold = 2.5; // threshold of significant in G's
const int numSamples = 128;

int samplesRead = 0;

namespace {
  const tflite::Model* model = nullptr;
  tflite::MicroInterpreter* interpreter = nullptr;
  TfLiteTensor* input = nullptr;
  TfLiteTensor* output = nullptr;

  constexpr int tensorArenaSize = 50000;
  alignas(16) uint8_t tensorArena[tensorArenaSize];
}  // namespace

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
    Serial.println(',');
} 

// array to map gesture index to a name

const char* GESTURES[] = {
  "WALKING",
  "WALKING_UPSTAIRS",
  "WALKING_DOWNSTAIRS",
  "SITTING",
  "STANDING",
  "LAYING"
};

#define NUM_GESTURES (sizeof(GESTURES) / sizeof(GESTURES[0]))

float calculateMax(float arr[]) {
  float res = arr[0];
  int length = sizeof(arr) / sizeof(arr[0]);

  for (int i = 0; i < sizeof(arr); ++i) 
    res = max(res, arr[i]);

  return res;
}

float calculateMin(float arr[]) {
  float res = arr[0];
  int length = sizeof(arr) / sizeof(arr[0]);

  for (int i = 0; i < sizeof(arr); ++i) 
    res = min(res, arr[i]);

  return res;
}

float scale(float val, float min, float max) {
  return (val - min) / (max - min);
}

void setup() {
  tflite::InitializeTarget();
  Serial.begin(9600);
  while (!Serial);


  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  IMU.setAccelerationSampleRate(2);
  IMU.setGyroscopeSampleRate(2);

  IMU.gyroUnit = RADIANSPERSECOND;

  // print out the samples rates of the IMUs
  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.print("Gyroscope sample rate = ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");


  // get the TFL representation of the model byte array
  model = tflite::GetModel(g_model);
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    Serial.println("Model provided is schema version not equal to supported version");
    return;
  }

  // static tflite::MicroMutableOpResolver<7> microOpResolver;
  // microOpResolver.AddConv2D();
  // microOpResolver.AddExpandDims();
  // microOpResolver.AddRelu();
  // microOpResolver.AddFullyConnected();
  // microOpResolver.AddSoftmax();
  // microOpResolver.AddReshape();

  static tflite::AllOpsResolver resolver;

  // Create an interpreter to run the model
  static tflite::MicroInterpreter staticInterpreter(model, resolver, tensorArena, tensorArenaSize);
  interpreter = &staticInterpreter;
  
  // Allocate memory for the model's input and output tensors
  TfLiteStatus allocateStatus = interpreter->AllocateTensors();
  if (allocateStatus != kTfLiteOk) {
    MicroPrintf(
        "Model provided is schema version %d not equal "
        "to supported version %d.",
        model->version(), TFLITE_SCHEMA_VERSION);
    return;
  }

  // Get pointers for the model's input and output tensors
  input = interpreter->input(0);
  output = interpreter->output(0);

  
}

void loop() {
  float aX, aY, aZ, gX, gY, gZ;

  // check if the all the required samples have been read since
  // the last time the significant motion was detected
  int count = 0;
  while (samplesRead < numSamples) {
    // check if both new acceleration and gyroscope data is
    // available
    if (!IMU.accelerationAvailable() || !IMU.gyroscopeAvailable())
      continue;

    // read the acceleration and gyroscope data
    // Accelerometer data between [-4, 4]
    // Gyroscopic data between [-2000, 2000] 
    IMU.readAcceleration(aX, aY, aZ);
    IMU.readGyroscope(gX, gY, gZ);

    float vals[6] = {gX, gY, gZ, aX, aY, aZ};
    float minVal = calculateMin(vals);
    float maxVal = calculateMax(vals);
    
    // Normalizing data between [0, 1] and setting it to the input tensor
    // Hawk Tuah!!
    input->data.f[samplesRead * 6 + 0] = scale(gX, minVal, maxVal);
    input->data.f[samplesRead * 6 + 1] = scale(gY, minVal, maxVal);
    input->data.f[samplesRead * 6 + 2] = scale(gZ, minVal, maxVal);
    input->data.f[samplesRead * 6 + 3] = scale(aX, minVal, maxVal);
    input->data.f[samplesRead * 6 + 4] = scale(aY, minVal, maxVal);
    input->data.f[samplesRead * 6 + 5] = scale(aZ, minVal, maxVal);
    
    
    // printData(input->data.f[samplesRead * 6 + 0], input->data.f[samplesRead * 6 + 1], input->data.f[samplesRead * 6 + 2], input->data.f[samplesRead * 6 + 3], input->data.f[
    // samplesRead * 6 + 4], input->data.f[samplesRead * 6 + 5]);
    samplesRead++;
  }

  TfLiteStatus invokeStatus = interpreter->Invoke();
  if (invokeStatus != kTfLiteOk) {
    Serial.println("Invoke failed!");
    while (1);
    return;
  }
  
  Serial.println();
  for (int i = 0; i < NUM_GESTURES; i++) {
    Serial.print(GESTURES[i]);
    Serial.print(": ");
    Serial.println(output->data.f[i]);
  }

  samplesRead = 0;
}


#include <Arduino_LSM9DS1.h>

const float accelerationThreshold = 2.25;
int SAMPLES = 300;
int samplesRead = 0;
int numSamples = 238;

void printData(float aX, float aY, float aZ, float gX, float gY, float gZ) {
  //print the data in CSV format
    Serial.print(aX, 3);
    Serial.print(' ');
    Serial.print(aY, 3);
    Serial.print(' ');
    Serial.print(aZ, 3);
    Serial.print(' ');
    Serial.print(gX, 3);
    Serial.print(' ');
    Serial.print(gY, 3);
    Serial.print(' ');
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

  // print out the samples rates of the IMUs
  // Serial.print("Accelerometer sample rate = ");
  // Serial.print(IMU.accelerationSampleRate());
  // Serial.println(" Hz");
  // Serial.print("Gyroscope sample rate = ");
  // Serial.print(IMU.gyroscopeSampleRate());
  // Serial.println(" Hz");
}

void loop() {
  float aX, aY, aZ, gX, gY, gZ;
  while (SAMPLES <= 0);

  // check if the all the required samples have been read since
  // the last time the significant motion was detected
  // wait for significant motion
  while (samplesRead == numSamples) {
    if (IMU.accelerationAvailable()) {
      // read the acceleration data
      IMU.readAcceleration(aX, aY, aZ);

      // sum up the absolutes
      float aSum = fabs(aX) + fabs(aY) + fabs(aZ);

      // check if it's above the threshold
      if (aSum >= accelerationThreshold) {
        // reset the sample read count
        samplesRead = 0;
        break;
      }
    }
  }

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

    aX = (aX + 4.0) / 8.0;
    aY = (aY + 4.0) / 8.0;
    aZ = (aZ + 4.0) / 8.0;

    gX = (gX + 2000.0) / 4000.0;
    gY = (gY + 2000.0) / 4000.0;
    gZ = (gZ + 2000.0) / 4000.0;

    printData(aX, aY, aZ, gX, gY, gZ);
    samplesRead++;
  }
  Serial.println();
  SAMPLES--;
}


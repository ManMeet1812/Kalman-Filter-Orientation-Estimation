#include <Arduino_LSM9DS1.h>

void setup() {
  Serial.begin(115200);
  delay(200);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.println("Accelerometer Roll & Pitch Measurement Started");
}

void loop() {

  float ax, ay, az;

  if (IMU.accelerationAvailable()) {

    IMU.readAcceleration(ax, ay, az);

    // -------- START TIMING (Algorithm Only) --------
    unsigned long t1 = micros();

    float roll  = atan2(ay, az) * 180.0 / PI;
    float pitch = atan2(-ax, sqrt(ay * ay + az * az)) * 180.0 / PI;

    unsigned long t2 = micros();
    unsigned long computationTime = t2 - t1;
    // -------- END TIMING --------

    // Print angles
    unsigned long time_ms = millis();
    Serial.print(time_ms);
    Serial.print(",ACC,");
    Serial.print(roll, 3);
    Serial.print(",");
    Serial.print(pitch, 3);
    Serial.print(",");
    Serial.println(computationTime);
  }
  delay(1000);

}

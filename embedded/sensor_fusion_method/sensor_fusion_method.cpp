#include <Arduino.h>
#include <Wire.h>
#include <Arduino_LSM9DS1.h>   // IMPORTANT

const float rad2deg = 180.0f / M_PI;

// ---------- Small helpers ----------
static inline float wrapPi(float a) {
  while (a >  M_PI) a -= 2.0f * M_PI;
  while (a < -M_PI) a += 2.0f * M_PI;
  return a;
}

// ---------- 1D Kalman filter ----------
class Kalman1D {
public:
  float Q_angle = 0.001f;
  float Q_bias  = 0.003f;
  float R_meas  = 0.03f;

  float angle = 0.0f;
  float bias  = 0.0f;
  float P00 = 0, P01 = 0, P10 = 0, P11 = 0;

  void setAngle(float a) { angle = a; }

  float update(float newAngle, float newRate, float dt) {
    float rate = newRate - bias;
    angle += dt * rate;

    P00 += dt * (dt*P11 - P01 - P10 + Q_angle);
    P01 -= dt * P11;
    P10 -= dt * P11;
    P11 += Q_bias * dt;

    float y = newAngle - angle;
    float S = P00 + R_meas;

    float K0 = P00 / S;
    float K1 = P10 / S;

    angle += K0 * y;
    bias  += K1 * y;

    float P00_temp = P00;
    float P01_temp = P01;

    P00 -= K0 * P00_temp;
    P01 -= K0 * P01_temp;
    P10 -= K1 * P00_temp;
    P11 -= K1 * P01_temp;

    return angle;
  }
};

Kalman1D kRoll;
Kalman1D kPitch;

unsigned long lastMicros = 0;
float yawEst = 0.0f;

// ---------- Read IMU ----------
bool readIMU(float &ax, float &ay, float &az,
             float &gx, float &gy, float &gz,
             float &mx, float &my, float &mz)
{
  if (!IMU.accelerationAvailable()) return false;
  if (!IMU.gyroscopeAvailable()) return false;
  if (!IMU.magneticFieldAvailable()) return false;

  IMU.readAcceleration(ax, ay, az);     // G
  IMU.readGyroscope(gx, gy, gz);        // deg/s
  IMU.readMagneticField(mx, my, mz);    // uT

  // Convert units
  ax *= 9.81f;
  ay *= 9.81f;
  az *= 9.81f;

  const float deg2rad = M_PI / 180.0f;
  gx *= deg2rad;
  gy *= deg2rad;
  gz *= deg2rad;

  return true;
}

void setup() {
  Serial.begin(115200);
  delay(200);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  IMU.setAccelerationRange(LSM9DS1_ACCELRANGE_2G);

  float ax, ay, az, gx, gy, gz, mx, my, mz;
  while (!readIMU(ax, ay, az, gx, gy, gz, mx, my, mz));

  float roll_acc  = atan2f(ay, az);
  float pitch_acc = atan2f(-ax, sqrtf(ay * ay + az * az));

  kRoll.setAngle(roll_acc);
  kPitch.setAngle(pitch_acc);

  lastMicros = micros();

  Serial.println("Kalman fusion running...");
}

void loop() {

  unsigned long now = micros();
  float dt = (now - lastMicros) * 1e-6f;
  lastMicros = now;
  if (dt <= 0) return;

  float ax, ay, az, gx, gy, gz, mx, my, mz;
  if (!readIMU(ax, ay, az, gx, gy, gz, mx, my, mz)) return;

  // ---------- START TIMING HERE ----------
  unsigned long t1 = micros();

  // 1) Accelerometer angles
  float roll_acc  = atan2f(ay, az);
  float pitch_acc = atan2f(-ax, sqrtf(ay * ay + az * az));

  // 2) Kalman filter
  float roll  = kRoll.update(roll_acc,  gx, dt);
  float pitch = kPitch.update(pitch_acc, gy, dt);

  // 3) Yaw calculation
  float mx_c = mx * cosf(pitch) + mz * sinf(pitch);
  float my_c = mx * sinf(roll) * sinf(pitch) +
               my * cosf(roll) -
               mz * sinf(roll) * cosf(pitch);

  float yaw_mag = atan2f(-my_c, mx_c);
  yawEst = wrapPi(yaw_mag);

  // ---------- STOP TIMING HERE ----------
  unsigned long t2 = micros();
  unsigned long computationTime = t2 - t1;


  //Serial.println("time_ms,method,roll_deg,pitch_deg,yaw_deg,compute_us");
  // after you compute roll,pitch,yawEst and computationTime
  Serial.print(millis()); Serial.print(",");
  Serial.print("FUS"); Serial.print(",");
  Serial.print(roll * rad2deg, 2); Serial.print(",");
  Serial.print(pitch * rad2deg, 2); Serial.print(",");
  Serial.print(yawEst * rad2deg, 2); Serial.print(",");
  Serial.println(computationTime);

  delay(1000);
}
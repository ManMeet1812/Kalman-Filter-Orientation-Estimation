# Embedded Code

This folder contains the embedded implementation for the two orientation-estimation methods developed on the **ESP32 / MacIoT platform** using the **LSM9DS1 IMU**.

## Subfolders
- **accelerometer_method/** — embedded code for accelerometer-only tilt estimation
- **sensor_fusion_method/** — embedded code for orientation estimation using accelerometer, gyroscope, and magnetometer data

## Purpose
The embedded code in this folder is responsible for:
- reading IMU sensor data from the LSM9DS1
- computing roll, pitch, and optionally yaw
- formatting output data for logging and analysis
- supporting real-time orientation estimation experiments

## Method Summary
### Accelerometer Method
Uses only accelerometer data to estimate tilt angles such as roll and pitch. This method is simple and works well in static conditions, but is less reliable during motion.

### Sensor Fusion Method
Combines accelerometer, gyroscope, and magnetometer data to improve stability, reduce drift, and support full 3D orientation estimation.

## Notes
This folder documents both embedded methods used in the project and supports comparison between simple tilt estimation and sensor-fusion-based orientation tracking.

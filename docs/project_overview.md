# Project Overview

## Project Title
Orientation Estimation Using Inertial and Magnetic Sensors with Sensor Fusion

## Summary
This project compares two approaches for estimating device orientation on an **ESP32/MacIoT platform** using the **LSM9DS1 IMU**:

1. **Accelerometer-Only Method**
2. **Sensor Fusion Method**

The goal was to evaluate how each method estimates orientation angles and to understand the trade-offs between simplicity, stability, drift, and dynamic performance. The project specifically compared a basic tilt-estimation method against a fused approach using accelerometer, gyroscope, and magnetometer data. 

## Team Members
- **Manmeet Kaur**
- **Dhvani Parikh** :contentReference[oaicite:1]{index=1}

## Team Contributions
### Dhvani Parikh
- Worked on the **accelerometer-only method**
- Implemented and analyzed tilt estimation using accelerometer data

### Manmeet Kaur
- Worked on the **sensor fusion method**
- Implemented and analyzed orientation estimation using accelerometer, gyroscope, and magnetometer data
- Supported comparison of fusion performance in terms of drift, stability, and computational behavior

## Objective
The objective of the project was to estimate **roll, pitch, and yaw** using inertial and magnetic sensor data, and to compare how a simple accelerometer-based approach differs from a sensor-fusion-based approach in both static and dynamic conditions. The sensor fusion method was designed to improve accuracy and stability by combining the strengths of multiple sensors. 

## Hardware and Tools
- **MacIoT Board (ESP32)**
- **LSM9DS1 IMU** (accelerometer + gyroscope + magnetometer)
- **PlatformIO** using Arduino framework
- **Arduino_LSM9DS1** library :contentReference[oaicite:3]{index=3}

## Method 1: Accelerometer-Only Orientation Estimation
The accelerometer method estimates **roll** and **pitch** using gravity-based tilt equations. This method works best when the system is relatively still and only gravity is acting on the sensor. It is simple and computationally light, but becomes unreliable during movement because the accelerometer also measures linear acceleration. It also cannot estimate **yaw** because gravity alone does not provide heading information. :contentReference[oaicite:4]{index=4}

### Strengths
- simple implementation
- low computational cost
- useful for static tilt measurement

### Limitations
- sensitive to vibration and motion
- inaccurate under linear acceleration
- cannot estimate yaw :contentReference[oaicite:5]{index=5}

## Method 2: Sensor Fusion Orientation Estimation
The sensor fusion method combines:
- **accelerometer** for long-term roll and pitch reference
- **gyroscope** for smooth short-term motion tracking
- **magnetometer** for yaw / heading reference

The fusion method was implemented to overcome the weaknesses of using any one sensor alone. A **Kalman filter** was used for roll and pitch estimation, while a tilt-compensated magnetometer-based yaw calculation was combined with gyro Z-rate information for smoother heading estimation. 

### Strengths
- better dynamic orientation tracking
- reduced drift compared to single-sensor methods
- full 3D orientation estimation including yaw
- smoother and more reliable results during motion

### Limitations
- more computationally complex
- requires calibration and filter tuning
- magnetometer readings can be affected by nearby metallic or electronic interference 

## Program Output
Both methods output results in **CSV-style format** to support analysis and visualization.

### Accelerometer Method Output
- `time_ms`
- `method`
- `roll_deg`
- `pitch_deg`
- `compute_us`

### Sensor Fusion Method Output
- `time_ms`
- `method`
- `roll_deg`
- `pitch_deg`
- `yaw_deg`
- `compute_us` 

## Python Analysis and Visualization
This project also includes Python scripts used to:
- process recorded data
- generate CSV-based outputs
- visualize angle behavior over time
- generate 3D orientation animations or graphs for result interpretation

These scripts support comparison between the accelerometer-only and sensor fusion methods.

## Applications
This type of orientation estimation is relevant to:
- robotics
- drones
- wearables
- AR/VR systems
- camera stabilization
- navigation systems :contentReference[oaicite:9]{index=9}

## Repository Purpose
This repository documents the code, analysis scripts, generated data, and result visuals for both orientation-estimation methods, with particular emphasis on my contribution to the **sensor fusion method**.

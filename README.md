# Orientation Estimation Using Inertial and Magnetic Sensors with Sensor Fusion

An embedded sensing project focused on estimating device orientation using IMU data on an ESP32/MacIoT platform, with comparison between an **accelerometer-only method** and a **sensor fusion method**.

## Project Overview
This project investigates two approaches for orientation estimation using inertial and magnetic sensor data:

- **Method 1: Accelerometer-Based Tilt Estimation**
- **Method 2: Sensor Fusion Using Accelerometer, Gyroscope, and Magnetometer**

The objective was to compare both methods in terms of orientation estimation capability, drift, computational efficiency, and performance in static and dynamic conditions.

## Team Members
This project was completed collaboratively by:

- **Manmeet Kaur**
- **Dhvani Parikh**

## Team Contributions
### Dhvani Parikh
- Worked on the **accelerometer-only method**
- Supported implementation and analysis for tilt estimation using accelerometer data

### Manmeet Kaur
- Worked on the **sensor fusion method**
- Implemented and analyzed orientation estimation using accelerometer, gyroscope, and magnetometer data
- Supported comparison of fusion performance in terms of accuracy, drift, and computational behavior

## Project Objective
The project aimed to estimate orientation angles such as **roll, pitch, and yaw** using IMU data and to understand how sensor fusion improves orientation estimation compared to using only one sensor source. The sensor fusion approach was designed to combine the strengths of different sensors while reducing their individual weaknesses.

## Methods

### Method 1: Accelerometer Method
The accelerometer-based method estimates tilt using gravity as a reference. This approach works well in static conditions but becomes less reliable during motion because the accelerometer measures both gravity and linear acceleration.

### Method 2: Sensor Fusion Method
The sensor fusion method combines:
- **accelerometer** for long-term roll/pitch reference
- **gyroscope** for smooth short-term motion tracking
- **magnetometer** for yaw / heading reference

This method uses filtering and fusion logic to provide more stable full-3D orientation estimation in dynamic conditions.

## Hardware / Platform
- ESP32 / MacIoT development platform
- LSM9DS1 inertial and magnetic sensor
- Embedded real-time orientation computation

## Key Topics
- IMU orientation estimation
- accelerometer-based tilt calculation
- gyroscope integration
- magnetometer heading reference
- sensor fusion
- Kalman filtering
- drift analysis
- computational efficiency analysis

## Results Summary
The project report concludes that:

- the **accelerometer-only method** is a strong baseline for low-cost static tilt estimation
- the **sensor fusion method** is better suited for full 3D orientation and dynamic motion tracking
- the fusion method can provide smoother and more informative orientation estimates, but requires proper filter tuning and calibration
- drift performance depends strongly on gyroscope bias estimation and Kalman tuning parameters 

## Applications
This type of orientation estimation is relevant to:
- mobile robots and drones
- AR/VR tracking
- wearables
- vehicle navigation assistance
- camera stabilization systems :contentReference[oaicite:2]{index=2}

## Repository Structure
```text
IMU-Orientation-Estimation-Sensor-Fusion/
├── README.md
├── src/
│   ├── accelerometer_method.cpp
│   └── sensor_fusion_method.cpp
├── results/
│   ├── static_test_plots.png
│   ├── dynamic_test_plots.png
│   └── drift_analysis.png
└── docs/
    └── project_overview.md

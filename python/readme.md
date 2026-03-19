# Python Scripts

This folder contains Python scripts used for **data processing, CSV generation, plotting, and visualization** for both orientation-estimation methods.

## Subfolders
- **accelerometer_method/** — Python scripts related to the accelerometer-only method
- **sensor_fusion_method/** — Python scripts related to the sensor fusion method

## Purpose
The scripts in this folder support:
- converting recorded outputs into CSV files
- plotting roll, pitch, and yaw data
- generating 2D angle graphs over time
- creating 3D orientation visualizations from recorded data
- comparing method behavior through offline analysis

## Script Types
Typical scripts in this folder may include:
- CSV generation scripts
- live or offline angle plotting scripts
- 3D graph / animation scripts
- result visualization utilities

## Notes
These Python files are used as supporting analysis tools alongside the embedded ESP32 / MacIoT code. They are intended to help interpret the output of the accelerometer and sensor fusion methods through graphs and visual playback.

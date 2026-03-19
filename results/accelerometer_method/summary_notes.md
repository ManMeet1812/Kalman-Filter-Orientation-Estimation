# Accelerometer Method Result Notes

## Summary
This folder contains result visuals for the **accelerometer-only orientation estimation method**.

## Files
- `static_accelerometer_test.png`
- `roll_dynamic_accelerometer_test.png`
- `pitch_dynamic_accelerometer_test.png`
- `animate_3d_orientation_accelerometer_method.mov`

## Observations
The accelerometer method estimates **roll** and **pitch** using gravity-based tilt calculations. It performs well in static conditions, where gravity remains the dominant measured acceleration.

During dynamic motion, the method becomes less reliable because the accelerometer also responds to linear acceleration. This introduces noise and reduces stability in the angle estimates.

## Key Takeaways
- works well for static tilt estimation
- simple and computationally efficient
- sensitive to motion and vibration
- cannot estimate yaw
- useful as a baseline for comparison with sensor fusion

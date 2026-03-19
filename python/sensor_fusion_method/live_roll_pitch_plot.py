import serial, time
import matplotlib.pyplot as plt
from collections import deque

PORT = "/dev/cu.SLAB_USBtoUART"   # change if needed
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

# rolling window size
N = 300
t = deque(maxlen=N)
roll = deque(maxlen=N)
pitch = deque(maxlen=N)
yaw = deque(maxlen=N)

plt.ion()
fig, ax = plt.subplots(3, 1, sharex=True)

line_r, = ax[0].plot([], [])
ax[0].set_ylabel("Roll (deg)")
ax[0].grid(True)

line_p, = ax[1].plot([], [])
ax[1].set_ylabel("Pitch (deg)")
ax[1].grid(True)

line_y, = ax[2].plot([], [])
ax[2].set_ylabel("Yaw (deg)")
ax[2].set_xlabel("Time (s)")
ax[2].grid(True)

t0 = None

print("Listening... expecting CSV: time_ms,method,roll_deg,pitch_deg,yaw_deg,compute_us")

while True:
    s = ser.readline().decode(errors="ignore").strip()
    if not s:
        continue

    # keep only CSV data rows
    if not s[0].isdigit():
        continue

    parts = s.split(",")
    if len(parts) < 6:
        continue

    ms = float(parts[0])
    r = float(parts[2])
    p = float(parts[3])
    y = float(parts[4])

    if t0 is None:
        t0 = ms
    ts = (ms - t0) / 1000.0

    t.append(ts)
    roll.append(r)
    pitch.append(p)
    yaw.append(y)

    # update plots
    line_r.set_data(t, roll)
    line_p.set_data(t, pitch)
    line_y.set_data(t, yaw)

    for a in ax:
        a.relim()
        a.autoscale_view()

    plt.pause(0.01)
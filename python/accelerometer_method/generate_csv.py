import serial, time

PORT = "/dev/cu.SLAB_USBtoUART"
BAUD = 115200
OUTFILE = "accel_static.csv"

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

with open(OUTFILE, "w") as f:
    f.write("time_ms,method,roll_deg,pitch_deg,compute_us\n")

    try:
        while True:  # run forever until Ctrl+C
            line = ser.readline().decode(errors="ignore").strip()
            if not line:
                continue

            # accept negative numbers too; just require 2 commas (3 fields)
            if line.count(",") >= 2:
                f.write(line + "\n")
                f.flush()
                print(line)

    except KeyboardInterrupt:
        print("\nStopped by user (Ctrl+C). Saving file...")

ser.close()
print(f"Saved {OUTFILE}.")
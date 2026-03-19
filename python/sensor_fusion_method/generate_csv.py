import serial, time

PORT = "/dev/cu.SLAB_USBtoUART"   
BAUD = 115200                    
OUTFILE = "fus_static.csv"
DURATION_SEC = 60

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

start = time.time()

with open(OUTFILE, "w") as f:
    f.write("time_ms,method,roll_deg,pitch_deg,yaw_deg,compute_us\n")

    while True:
        # stop after 60 seconds
        if time.time() - start >= DURATION_SEC:
            break

        line = ser.readline().decode(errors="ignore").strip()
        if not line:
            continue

        # keep only CSV data rows (skip boot/debug text)
        if line[0].isdigit() and line.count(",") >= 4:
            f.write(line + "\n")
            f.flush()
            print(line)

ser.close()
print(f"Saved {OUTFILE} (60 seconds).")
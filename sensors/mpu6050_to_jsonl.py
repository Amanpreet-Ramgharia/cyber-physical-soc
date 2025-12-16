# MPU6050 (software I2C) → JSONL
# Emits: iot.device.tamper
#
# Wiring (software I2C):
#   SDA -> GPIO21
#   SCL -> GPIO20
#   VCC -> 3.3V
#   GND -> GND
#
# Notes:
# - Ensure software I2C is enabled (see docs/pi_setup.md)
# - Device address often 0x68 (or 0x69 depending on AD0)

import time
import socket
import math
from collections import deque
from smbus2 import SMBus

from sensors.common.jsonl_logger import append_jsonl, base_event

# ---- CONFIG ----
I2C_BUS = 3          # change if your /dev/i2c-* differs
ADDRESS = 0x68       # change to 0x69 if i2cdetect shows 69
OUTFILE = "/home/pi/iot/mpu_events.jsonl"
LOCATION = "desk"
SENSOR = "mpu6050-desk-1"
HOST = socket.gethostname()

# Detection tuning
WINDOW = 10                  # moving average window
DELTA_THRESHOLD = 0.25       # tune per environment
COOLDOWN_SECONDS = 2         # avoid event spam
SAMPLE_DELAY = 0.1

# MPU6050 registers
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B

def read_word(bus, reg):
    high = bus.read_byte_data(ADDRESS, reg)
    low = bus.read_byte_data(ADDRESS, reg + 1)
    val = (high << 8) + low
    if val >= 0x8000:
        val = -((65535 - val) + 1)
    return val

def read_accel_g(bus):
    # Raw accel scale for +/-2g is 16384 LSB/g
    ax = read_word(bus, ACCEL_XOUT_H) / 16384.0
    ay = read_word(bus, ACCEL_XOUT_H + 2) / 16384.0
    az = read_word(bus, ACCEL_XOUT_H + 4) / 16384.0
    return ax, ay, az

def magnitude(ax, ay, az):
    return math.sqrt(ax*ax + ay*ay + az*az)

def main():
    mv = deque(maxlen=WINDOW)
    last_emit = 0.0

    with SMBus(I2C_BUS) as bus:
        # Wake up MPU6050
        bus.write_byte_data(ADDRESS, PWR_MGMT_1, 0)

        # Prime window
        for _ in range(WINDOW):
            ax, ay, az = read_accel_g(bus)
            mv.append(magnitude(ax, ay, az))
            time.sleep(SAMPLE_DELAY)

        baseline = sum(mv) / len(mv)

        while True:
            ax, ay, az = read_accel_g(bus)
            mag = magnitude(ax, ay, az)
            mv.append(mag)
            avg = sum(mv) / len(mv)
            delta = abs(avg - baseline)

            # Slowly adapt baseline (prevents drift)
            baseline = (baseline * 0.98) + (avg * 0.02)

            now = time.time()
            if delta >= DELTA_THRESHOLD and (now - last_emit) >= COOLDOWN_SECONDS:
                evt = base_event(
                    event_type="iot.device.tamper",
                    sensor=SENSOR,
                    location=LOCATION,
                    host=HOST,
                )
                evt.update({
                    "ax": round(ax, 4),
                    "ay": round(ay, 4),
                    "az": round(az, 4),
                    "magnitude_g": round(mag, 4),
                    "moving_avg_g": round(avg, 4),
                    "baseline_g": round(baseline, 4),
                    "delta": round(delta, 4),
                    "threshold": DELTA_THRESHOLD,
                })
                append_jsonl(OUTFILE, evt)
                last_emit = now

            time.sleep(SAMPLE_DELAY)

if __name__ == "__main__":
    main()

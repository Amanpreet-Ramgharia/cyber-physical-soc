# PIR HC-SR501 → JSONL
# Emits: iot.motion.detected
#
# Wiring:
#   OUT -> GPIO17
#   VCC -> 5V (module commonly expects 5V)
#   GND -> GND

import time
import socket
from gpiozero import MotionSensor

from sensors.common.jsonl_logger import append_jsonl, base_event

# ---- CONFIG ----
GPIO_PIN = 17
OUTFILE = "/home/pi/iot/pir_events.jsonl"
LOCATION = "desk"
SENSOR = "pir-1"
HOST = socket.gethostname()

# Debounce/tuning parameters
QUEUE_SECONDS = 0.5  # smoothing
PIR_COOLDOWN = 2     # avoid event spam

pir = MotionSensor(GPIO_PIN, queue_len=int(max(1, QUEUE_SECONDS * 10)))

def main():
    last_emit = 0.0
    while True:
        pir.wait_for_motion()
        now = time.time()
        if now - last_emit >= PIR_COOLDOWN:
            evt = base_event(
                event_type="iot.motion.detected",
                sensor=SENSOR,
                location=LOCATION,
                host=HOST,
            )
            evt.update({"motion": True})
            append_jsonl(OUTFILE, evt)
            last_emit = now

        pir.wait_for_no_motion()
        time.sleep(0.05)

if __name__ == "__main__":
    main()

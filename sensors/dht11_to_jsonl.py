# DHT11 → JSONL
# Emits: iot.env.reading
#
# Wiring:
#   DATA -> GPIO5
#   VCC  -> 3.3V (or 5V per module spec)
#   GND  -> GND
#   Pull-up resistor between DATA and VCC (commonly 4.7k–10k)

import time
import socket
import board
import adafruit_dht

from sensors.common.jsonl_logger import append_jsonl, base_event

# ---- CONFIG ----
GPIO_PIN = board.D5
OUTFILE = "/home/pi/iot/dht11_events.jsonl"
LOCATION = "desk"
SENSOR = "dht11-1"
HOST = socket.gethostname()
INTERVAL_SECONDS = 5

dht = adafruit_dht.DHT11(GPIO_PIN)

def main():
    while True:
        try:
            temp_c = dht.temperature
            humidity = dht.humidity
            if temp_c is not None and humidity is not None:
                evt = base_event(
                    event_type="iot.env.reading",
                    sensor=SENSOR,
                    location=LOCATION,
                    host=HOST,
                )
                evt.update({
                    "temperature_c": float(temp_c),
                    "humidity": float(humidity),
                })
                append_jsonl(OUTFILE, evt)
            time.sleep(INTERVAL_SECONDS)

        except RuntimeError:
            # DHT sensors can be noisy; retry next interval
            time.sleep(1)
        except Exception as e:
            # Don't crash permanently—log and continue
            evt = base_event(
                event_type="iot.env.error",
                sensor=SENSOR,
                location=LOCATION,
                host=HOST,
            )
            evt.update({"error": str(e)})
            append_jsonl(OUTFILE, evt)
            time.sleep(2)

if __name__ == "__main__":
    main()

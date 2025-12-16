# Cyber-Physical SOC (Raspberry Pi Sensors → Splunk SIEM → Incidents)

Treat **physical events** (motion, vibration/tamper, temperature/humidity) as **security telemetry**, forward them to **Splunk**, correlate signals, and automatically create **SOC-style incidents**.

> Built for: SOC / Detection Engineering portfolio, research prototype, and PhD proposal context.

---

## Architecture

**Sensors → Raspberry Pi → JSONL logs → Splunk Universal Forwarder → Splunk (SIEM)**
- Sensors write newline-delimited JSON (`.jsonl`) under: `/home/pi/iot/`
- Universal Forwarder tails the JSONL files and sends to Splunk
- Splunk indexes raw telemetry in `iot`
- A correlation search detects **Motion + Tamper within 120s**
- Alert action logs an incident into `incidents` (or sends to HEC)

---

## Hardware

- Raspberry Pi 3 B+
- Breadboard, GPIO extender, jumper wires
- **DHT11** (temp/humidity) → GPIO5 (with pull-up resistor)
- **PIR HC-SR501** (motion) → GPIO17
- **MPU6050** (vibration/tamper, software I2C) → SDA GPIO21, SCL GPIO20

---

## Raspberry Pi Setup

### 1) OS + Python venv
```bash
sudo apt update
sudo apt install -y python3-venv python3-smbus i2c-tools
python3 -m venv ~/iot-venv --system-site-packages
source ~/iot-venv/bin/activate
pip install -r requirements.txt
```

### 2) Enable software I2C (Bookworm / Debian 12)
See `docs/pi_setup.md` for the exact steps and config snippets.

### 3) Run sensors
```bash
source ~/iot-venv/bin/activate
python sensors/dht11_to_jsonl.py
python sensors/pir_to_jsonl.py
python sensors/mpu6050_to_jsonl.py
```

Optional: install systemd services from `services/` to run on boot.

---

## Splunk Setup

### Indexes
- `iot` → raw sensor telemetry
- `incidents` → correlated incidents

### Sourcetypes
- `iot:dht11:json`
- `iot:pir:json`
- `iot:mpu:json`
- `incident:json`

See:
- `splunk/indexes.conf`
- `splunk/props.conf`
- `splunk/uf_inputs.conf` (for the Pi Universal Forwarder)

---

## Detection & Correlation (SOC-style)

Core idea: **reduce false positives** by requiring multiple signals.

**Condition**
- PIR motion AND MPU tamper within **120 seconds**

Artifacts:
- Correlation SPL: `splunk/searches/correlation_motion_and_tamper.spl`
- Saved search stanza: `splunk/savedsearches.conf`

---

## Incident Response Automation

Two methods included:

1) **Write incident to `incidents` index** (native Splunk alert action via summary indexing)
2) **Send incident JSON via HEC** (SOAR-ready)

HEC sender:
- `incident-response/hec_sender.py`
- Schema: `incident-response/incident_schema.json`

---

## Dashboards

Starter dashboards + panels live in:
- `splunk/dashboards/`

Includes:
- Environment telemetry
- Motion timeline
- Tamper timeline
- Correlation panel
- Incidents panel (lifecycle starter)

---



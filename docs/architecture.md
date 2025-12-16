# Architecture

## End-to-End Flow
1. Physical sensors generate events
2. Raspberry Pi reads sensors and writes JSONL to `/home/pi/iot/`
3. Splunk Universal Forwarder tails JSONL files and forwards to Splunk
4. Splunk indexes:
   - `iot` for raw telemetry
   - `incidents` for correlated incident records
5. Correlation search runs on a schedule and creates incidents

## Why JSONL?
- Easy to tail
- One event per line
- Plays nicely with forwarders and line breakers

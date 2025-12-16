"""
Send incident events to Splunk via HTTP Event Collector (HEC).

Usage:
  export SPLUNK_HEC_URL="https://<splunk-host>:8088/services/collector/event"
  export SPLUNK_HEC_TOKEN="<token>"
  python incident-response/hec_sender.py --event-file incident-response/sample_incident.json
"""

import argparse
import json
import os
import sys
import requests

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--event-file", required=True, help="Path to JSON file containing the incident payload")
    p.add_argument("--index", default="incidents", help="Splunk index for event metadata")
    p.add_argument("--sourcetype", default="incident:json", help="Splunk sourcetype")
    args = p.parse_args()

    url = os.environ.get("SPLUNK_HEC_URL")
    token = os.environ.get("SPLUNK_HEC_TOKEN")
    if not url or not token:
        print("Missing SPLUNK_HEC_URL or SPLUNK_HEC_TOKEN env vars.", file=sys.stderr)
        sys.exit(2)

    with open(args.event_file, "r", encoding="utf-8") as f:
        payload = json.load(f)

    hec_event = {"index": args.index, "sourcetype": args.sourcetype, "event": payload}

    headers = {"Authorization": f"Splunk {token}", "Content-Type": "application/json"}

    # In production, set verify=True and use a valid cert.
    resp = requests.post(url, headers=headers, data=json.dumps(hec_event), timeout=10, verify=False)
    resp.raise_for_status()
    print("Sent incident to HEC:", resp.text)

if __name__ == "__main__":
    main()

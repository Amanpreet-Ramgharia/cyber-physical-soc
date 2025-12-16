# Detection & Correlation Logic

## Rule
Create an incident when:
- PIR motion occurs, and
- MPU tamper occurs
- both within a 120-second window

See:
- `splunk/searches/correlation_motion_and_tamper.spl`
- `splunk/savedsearches.conf`

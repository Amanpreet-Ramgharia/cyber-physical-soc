# CP-SOC Splunk App (Packaging)

This folder is a **Splunk app package layout** so you can import dashboards, saved searches, and macros in one go.

## Import / Install
1. Copy `CP_SOC/` to:
   - Linux: `$SPLUNK_HOME/etc/apps/CP_SOC`
   - Windows: `C:\Program Files\Splunk\etc\apps\CP_SOC`
2. Restart Splunk.

## Contents
- Dashboards: `default/data/ui/views/*.xml`
- Navigation menu: `default/data/ui/nav/default.xml`
- Correlation macro + saved search: `default/macros.conf`, `default/savedsearches.conf`
- Parsing settings: `default/props.conf`

## Important notes (indexes.conf)
`indexes.conf` is included for reference, but indexes should typically be created on the **indexer** (or Splunk Cloud via UI/support),
not blindly deployed from an app. If you're on Splunk Enterprise single-instance, it's fine to apply.


---
phase: 2
plan: 2
wave: 1
---

# Plan 2.2: Robust Vendor Submissions

## Objective
Improve the reliability of user-submitted vendors by enhancing Google Maps URL parsing, including support for shortened URLs and better coordinate extraction.

## Context
- app/routes/main.py
- requirements.txt

## Tasks

<task type="auto">
  <name>Enhance Google Maps URL Parsing</name>
  <files>
    - app/routes/main.py
  </files>
  <action>
    1. Update the `submit_vendor` route's parsing logic.
    2. Add support for `requests` to follow redirects for `goo.gl` or `maps.app.goo.gl` links to extract the full URL.
    3. Improve regex patterns to handle various coordinate formats (e.g., `!3d` vs `@`).
    4. Ensure coordinates are validated (lat between -90 and 90, lng between -180 and 180).
  </action>
  <verify>Submit a 'maps.app.goo.gl' link and verify coordinates are extracted in the database.</verify>
  <done>Successful coordinate extraction for at least 3 different Google Maps URL formats.</done>
</task>

## Success Criteria
- [ ] Shortened Google Maps URLs are resolved and parsed correctly.
- [ ] Coordinates are validated before being saved to the database.

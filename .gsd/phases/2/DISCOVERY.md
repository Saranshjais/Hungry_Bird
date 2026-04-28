# Phase 2 Discovery: Performance & Reliability

## Caching Strategy
Given the project scale, a heavy Redis setup is overkill. 
- **Option A**: `flask-caching` with `SimpleCache` (in-memory).
- **Option B**: Manual dictionary caching in `ml_model.py`.
- **Decision**: Use `flask-caching` with `FileSystemCache`. This persists across restarts and is easy to set up without external dependencies.

## Google Maps URL Parsing
Common formats to support:
1. `@lat,lng` (Search results/Browser URL)
2. `!3dLAT!4dLNG` (Direct link)
3. `q=lat,lng` (Legacy/Embed)
4. `maps.app.goo.gl` (Short links) - **Needs resolution via requests HEAD.**

## Error Handling
The ML model should fail gracefully. If `vendor_list` is too small or if `TfidfVectorizer` fails (e.g., empty features), it should return an empty list rather than crashing.

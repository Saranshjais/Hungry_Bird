---
phase: 2
plan: 1
wave: 1
---

# Plan 2.1: ML Performance & Stability

## Objective
Reduce server load by caching recommendation results and ensuring the ML pipeline is robust against edge cases (empty data, small sets).

## Context
- .gsd/SPEC.md
- .gsd/ARCHITECTURE.md
- app/routes/main.py
- app/ml_model.py

## Tasks

<task type="auto">
  <name>Implement ML Caching</name>
  <files>
    - requirements.txt
    - app/__init__.py
    - app/routes/main.py
  </files>
  <action>
    1. Add `Flask-Caching` to `requirements.txt`.
    2. Initialize `Cache(config={'CACHE_TYPE': 'FileSystemCache', 'CACHE_DIR': 'instance/cache'})` in `app/__init__.py`.
    3. Use `@cache.memoize(timeout=3600)` on a wrapper function for `build_recommendation_model` in `main.py` or directly if appropriate.
    4. Ensure the cache key includes the city slug.
  </action>
  <verify>Check `instance/cache` directory after visiting a city page multiple times.</verify>
  <done>City page load time (TTFB) is significantly lower on subsequent visits.</done>
</task>

<task type="auto">
  <name>ML Robustness & Error Handling</name>
  <files>
    - app/ml_model.py
  </files>
  <action>
    1. Add validation to `build_recommendation_model` to return early if `vendors` count < 2.
    2. Wrap `TfidfVectorizer` fit in a try-except block to handle cases where all features are stop-words or empty.
    3. Ensure `get_recommendations` handles missing vendor names gracefully without indexing errors.
  </action>
  <verify>Manually trigger a city page with only 1 vendor and ensure it doesn't 500.</verify>
  <done>ML functions return safe defaults (empty lists/dfs) on failure.</done>
</task>

## Success Criteria
- [ ] Recommendation engine is cached for at least 1 hour per city.
- [ ] Application does not crash when processing cities with very few vendors.

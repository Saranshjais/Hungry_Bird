# ROADMAP.md

> **Current Milestone**: MVP (v1.0)
> **Goal**: Establish core discovery and recommendation features with performance stability.

## Must-Haves
- [ ] Vendor listing by city
- [ ] Cuisine-based recommendation engine
- [ ] Google Maps integration
- [ ] User submission form

## Phases

### Phase 1: Core Discovery Foundation
**Status**: ✅ Completed
**Objective**: Build basic Flask structure, database models, and recommendation logic.

---

### Phase 2: Performance & Reliability Polish
**Status**: ✅ Complete
**Objective**: Improve the efficiency of the recommendation engine and the robustness of the submission pipeline.

**Tasks**:
- [ ] **ML Caching**: Implement caching for recommendation results.
- [ ] **Robust Maps Parsing**: Upgrade the Google Maps URL parser.
- [ ] **Error Handling**: Add global error boundaries for the recommendation engine.

**Verification**:
- Benchmarking page load times before/after caching.
- Test suite for various Google Maps URL formats.

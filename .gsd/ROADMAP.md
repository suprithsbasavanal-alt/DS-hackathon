---
milestone: BreatheWise Complete AI Expansion
version: 2.0.0
updated: 2026-11-16T13:05:00+05:30
---

# BreatheWise Complete AI Expansion — Roadmap

> **Current Phase:** Phase A — Specification & Adversarial EGM Review  
> **Status:** Planning Only (Code Freeze in Effect until User Approval)  
> **Execution Rule:** One atomic task per commit with automated test and regression verification.

---

## Must-Haves (from SPEC.md)

- [ ] **MH-01:** Raw data integrity: zero modifications to `data/raw/` files; derived artifacts 100% reproducible.
- [ ] **MH-02:** Strict averaging period compliance: daily CO and $\text{O}_3$ excluded from daily station AQI; 8h rolling values restricted to landmark hourly slices with project 6-of-8 rule.
- [ ] **MH-03:** Lead (Pb) transparency: displayed as `"Not available in supplied dataset"`, never zero or imputed.
- [ ] **MH-04:** Non-causal associations: Pearson and Spearman weather correlations reported as retrospective associations with sample counts ($N$).
- [ ] **MH-05:** Exploratory environmental clustering: evaluated with silhouette scores and sample size checks; automated fallback to descriptive quantiles if unstable.
- [ ] **MH-06:** Deterministic health advisories: auditable rule IDs (`RULE-*`), explicit triggers, supporting pollutant/AQI values, and non-medical disclaimers.
- [ ] **MH-07:** Physics-based purification simulator: idealized well-mixed equation $C(t) = C_0 \times \exp(-\frac{\text{CADR}}{V} \times t)$ with boundary validation; explicitly labeled as non-AI theoretical what-if scenario.
- [ ] **MH-08:** Backwards-compatible FastAPI endpoints: Pydantic schemas, input validation, and zero disruption to existing 9 endpoints.
- [ ] **MH-09:** Premium responsive frontend: new `AIInsightsView.tsx` and `PurificationSimulator.tsx` using Google Stitch tokens.
- [ ] **MH-10:** 100% offline-first operation: zero external cloud dependencies or remote LLM calls; all 60 existing tests + new test suite passing.

---

## Phases & Atomic Tasks

### Phase A: Specification & Adversarial Review (Current Phase)
**Status:** 🔄 In Progress (Planning Only)  
**Objective:** Finalize specification, roadmap, implementation contracts, threshold matrix, model cards, and run independent EGM Goldfish review.  
**Dependencies:** None  
- [x] **Task A.1:** Finalize `.gsd/SPEC.md` with complete scientific boundaries, API schemas, and simulator math.
- [x] **Task A.2:** Finalize `.gsd/ROADMAP.md` with dependency-ordered phases and atomic tasks.
- [x] **Task A.3:** Author Data, Averaging-Period & Threshold Matrix across all 7 pollutants and 6 weather parameters.
- [x] **Task A.4:** Author Machine Learning Model Card for Unsupervised Environmental Regimes (clustering & fallback).
- [x] **Task A.5:** Author Physics Model Card for Theoretical Air Purification Simulator.
- [x] **Task A.6:** Invoke independent EGM Hostile Design Critic (`egm-design`) subagent for adversarial review.
- [ ] **Task A.7:** Request explicit user authorization before proceeding to implementation.

---

### Phase B: Data & Threshold Foundation
**Status:** 🟢 Complete (Verified with 74 Passing Tests)  
**Objective:** Implement Pydantic validation contracts, threshold adapters, and environmental data aggregation.  
**Dependencies:** Phase A approval  
- [x] **Task B.1:** Create `backend/schemas/` (`environmental.py`, `regimes.py`, `health.py`, `purification.py`) defining typed request/response contracts.
- [x] **Task B.2:** Implement `backend/threshold_engine.py` connecting criteria pollutants to `cpcb_calculator.py` with unit verification, ensuring daily 24h CO/O3 sub-indices are strictly null.
- [x] **Task B.3:** Implement `backend/environmental_analysis.py` computing unified multi-pollutant summaries and correlation matrices with sample counts ($N=670$).
- [x] **Task B.4:** Create `backend/test_environmental.py` validating threshold tiers, Pb absence handling, unit conversions, 24h CO/O3 null sub-indices, invalid stations, invalid dates, and correlation sample counts.
- [x] **Task B.5:** Mount `GET /api/ai/insights` in `backend/main.py` with station and date validation, verified against regression suites.

---

### Phase C: Exploratory Environmental Regimes
**Status:** 🟢 Complete (Verified with 82 Passing Tests)  
**Objective:** Implement unsupervised environmental clustering with silhouette optimization and automated fallback.  
**Dependencies:** Phase B  
- [x] **Task C.1:** Create `backend/schemas/regimes.py` defining regime profiles and diagnostic schemas.
- [x] **Task C.2:** Implement `backend/environmental_regimes.py` with 8 standardized features (using orthogonal wind vectors $u, v$ without redundant scalar wind speed), $k$-Means ($k \in [2, 5]$), silhouette heuristic gating ($S \ge 0.30$, min cluster $\ge 5\%$), and deterministic seasonal fallback.
- [x] **Task C.3:** Precompute and serialize `data/processed/environmental_regimes.json` ensuring 100% offline reproducibility and sub-millisecond API response.
- [x] **Task C.4:** Create `backend/test_regimes.py` verifying cluster stability, silhouette threshold handling, and fallback behavior.
- [x] **Task C.5:** Mount `GET /api/ai/regimes` in `backend/main.py` serving cached precomputed static JSON.

---

### Phase D: Decision Support Engines (Health & Purification)
**Status:** ⬜ Not Started  
**Objective:** Implement deterministic CPCB health advisory engine and validated first-order purification decay engine.  
**Dependencies:** Phase B  
- [ ] **Task D.1:** Create `backend/schemas/health.py` and `backend/schemas/purification.py` (allowing CADR $\ge 0$, runtime $\ge 0$).
- [ ] **Task D.2:** Implement `backend/health_advisor.py` with deterministic CPCB category mapping, rule IDs (`RULE-AQI-*`, `RULE-PM*`), and trigger evidence.
- [ ] **Task D.3:** Implement `backend/purification_simulator.py` with first-order decay equation, 40-point curve generation, boundary checks, and assumption disclosures.
- [ ] **Task D.4:** Create `backend/test_health_advisor.py` validating all rule triggers, evidence formatting, and disclaimers.
- [ ] **Task D.5:** Create `backend/test_purification.py` verifying CADR=0, t=0, negative-dimension rejection, and monotonic decay.

---

### Phase E: API & Frontend Integration
**Status:** ⬜ Not Started  
**Objective:** Mount new endpoints in FastAPI and build responsive React views using Google Stitch tokens.  
**Dependencies:** Phases B, C, D  
- [ ] **Task E.1:** Register `/api/ai/insights`, `/api/ai/regimes`, `/api/ai/health-advisory`, and `/api/purification/simulate` in `backend/main.py`.
- [ ] **Task E.2:** Create `backend/test_ai_endpoints.py` testing all new routes with valid, boundary (CADR=0, t=0), and invalid inputs.
- [ ] **Task E.3:** Update TypeScript API client (`frontend/src/services/api.ts`) and type definitions (`frontend/src/types/index.ts`).
- [ ] **Task E.4:** Implement `frontend/src/components/PurificationSimulator.tsx` with interactive controls, 40-point decay chart, and mathematical disclosures rendered via semantic HTML.
- [ ] **Task E.5:** Implement `frontend/src/views/AIInsightsView.tsx` synthesizing threshold tables, weather associations, regimes, and health rules.
- [ ] **Task E.6:** Update `frontend/src/App.tsx` navigation bar and hash router (`#ai-insights`) with responsive padding to prevent layout wrapping on tablet viewports.
- [ ] **Task E.7:** Build production frontend bundle (`npm run build`) and verify static asset mounting.

---

### Phase F: Verification, Offline Audit & Documentation
**Status:** ⬜ Not Started  
**Objective:** Execute full automated test suite, capture visual evidence, verify offline operation, and update documentation.  
**Dependencies:** Phase E  
- [ ] **Task F.1:** Execute full pytest suite (`backend/test_*.py`) ensuring zero regressions across all 60 existing + new tests.
- [ ] **Task F.2:** Capture high-resolution desktop and mobile viewport screenshots of new views (`screenshots/ai_insights.png`, `screenshots/purification_simulator.png`).
- [ ] **Task F.3:** Execute offline verification protocol (disconnect network, launch `./venv/bin/uvicorn backend.main:app`, verify zero network errors).
- [ ] **Task F.4:** Update `PRD.md`, `architecture.md`, `design.md`, `phase.md`, `memory.md`, and `README.md`.
- [ ] **Task F.5:** Author comprehensive verification report artifact with empirical evidence.

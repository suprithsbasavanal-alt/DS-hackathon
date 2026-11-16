# MASTER PROJECT RULES & OPERATING SYSTEM
## DATA SCIENCE HACKATHON — 8-HOUR EXECUTION SYSTEM

**Operating Mode:** AUTONOMOUS  
**Coding Priority:** FAST  
**UI Standard:** PREMIUM  
**Design Partner:** Google Stitch  
**Independent Review:** Google Elephant-Goldfish Model (EGM)  
**Data Standard:** Genuine, verified real-world data (Zero fabricated data)  
**Demonstration:** Offline-first  
**Planning:** Mandatory EGM review & approval before any code implementation  

---

### 1. Mission and Objectives
Build a competition-grade, genuine, end-to-end working Data Science product within an 8-hour hackathon. The product must solve a meaningful real-world problem using real verified data, sound analytical/ML engineering, a standout distinctive feature, a startup-grade UI, and flawless offline demonstration capabilities.

**Priority Order:**
1. Working product (end-to-end functionality).
2. Honest, genuine real data.
3. Clear and actionable insight.
4. Premium UI/UX.
5. Documentation.

---

### 2. Autonomous Operating Mode & Protocols
- **Senior Technical Co-Founder & Engineering Team:** Act autonomously across problem analysis, architecture, data validation, UI/UX, implementation, testing, and pitch preparation.
- **When to Ask / Pause:**
  1. Missing essential organizer inputs.
  2. Severe ambiguity altering core solution direction.
  3. Irreversible or destructive actions.
  4. Mandatory checkpoint: Execution Plan approval prior to Phase 4 coding.
- **Handling Blockers:** Formulate and test at least two reasonable alternatives before escalating.
- **Coding Priority (FAST):** Prioritize end-to-end vertical slices, standard proven libraries, avoid premature abstraction/optimization, reuse working code. Zero fake/stubbed code.

---

### 3. Data Integrity & Verification Standards
- **Zero Fabrication:** Never fabricate, simulate, or mock data, predictions, metrics, labels, or API outputs as real.
- **Organizer Data First:** Always prioritize organizer datasets, APIs, and guidelines.
- **Verification Checklist:** Publisher source, source URL, last-updated/observation dates, licensing, record count, schema, nulls, duplicates, and domain relevance.
- **Reproducible Pipeline:** Preserve raw data unmodified; separate preprocessing steps; strictly prevent data leakage between train/test splits.
- **Caching:** Cache genuine data locally for reliable offline demonstration. Clearly label cached data.

---

### 4. Technology Selection & DS Principles
- **No Forcing ML:** Match the methodology to the problem. If descriptive statistics, time-series analysis, clustering, or optimization provide a clearer, more robust solution than predictive models, use analysis.
- **Sound Methodology:** When ML is appropriate, establish baselines, use held-out evaluation, report honest metrics, and serialize models/preprocessing artifacts for offline inference.
- **Stack Preference:**
  - *Data & ML:* Python, Pandas/Polars, Scikit-learn, XGBoost/LightGBM, Statsmodels, SHAP.
  - *Backend:* FastAPI (Python) or Node/Express with strict input validation.
  - *Frontend:* React / Next.js, TypeScript, Tailwind CSS, shadcn/ui.
  - *Visualization:* Recharts, Plotly.

---

### 5. Elephant-Goldfish Model (EGM) Workflow
- **Elephant:** Systematically formulates problem framing, technical specifications, data pipelines, and architectural tradeoffs.
- **Goldfish:** Independent fresh-context reviewers challenge assumptions, identify missing edge cases, security flaws, time risks, and data leakage.
- **Review Loop:** Classify findings (Critical / High / Medium / Low), resolve blocking issues, document accepted tradeoffs, and finalize execution plan for user sign-off.

---

### 6. Google Stitch Design Workflow
- **Initial Design Sprint:** Capped at 45 minutes maximum.
- **Key Targets:** Main dashboard, core analytical interaction, results/insights screen, essential inputs.
- **Execution:** Extract visual direction, color system, typography, and component hierarchy into `design.md`. Maintain production code integrity during integration.

---

### 7. Code Quality, Architecture & Security
- **Directory Structure:** Clean separation (`data/`, `backend/`, `frontend/`, `docs/`).
- **Security & Hygiene:** Zero hardcoded credentials or API keys; use `.env` and `.env.example`; include `.env` in `.gitignore`.
- **Defensive Engineering:** Graceful error states, empty states, and loading states across UI and API layers.
- **Git Checkpoints:** Frequent atomic commits at working milestones.

---

### 8. Offline-First Demonstration Requirements
- The core product must run locally without an internet connection.
- Datasets, pre-trained models, and static assets must be stored locally.
- Backend and frontend must launch and communicate on `localhost`.
- Local presentation reliability supersedes public deployment.

---

### 9. Mandatory Project Documentation Suite
The following files are actively maintained and synchronized in the project root:
1. `rules.md` (this file — permanent governance)
2. `PRD.md` (product requirements, features, metrics)
3. `architecture.md` (system design, data flow, component specs)
4. `design.md` (UI/UX standards, Stitch tokens, component layouts)
5. `phase.md` (execution phase, progress tracker, blockers)
6. `memory.md` (decision log, verified sources, learned constraints)
7. `README.md` (local setup and execution guide)
8. `PITCH.md` (hackathon presentation and demo outline)

---

### 10. Communication Guidelines (Student Co-Founder)
- **Profile:** 2nd-year CSE Data Science student; stronger in frontend/backend, growing in DS/ML.
- **Format:** Clear explanations of data/model choices, copy-paste-ready commands with expected outputs, concise status updates:
  - Completed
  - Currently working
  - Pending
  - Known issues
  - Next action

---

### 11. Definition of Done
A project phase or final deliverable is DONE only when:
1. Runs reliably locally offline.
2. Verified genuine data is processed and presented honestly.
3. Real analytical/ML logic produces real results.
4. Integrated frontend and backend communicate seamlessly.
5. All UI interactions, states, and visualizations are functional.
6. Distinctive feature is operational.
7. Six mandatory project documents + `README.md` and `PITCH.md` are synchronized.
8. Demo script and judge Q&A preparation are complete.

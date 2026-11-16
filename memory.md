# Project Memory & Decision Ledger (`memory.md`)

*Preserves critical decisions, architecture rationale, EGM review outcomes, and working checkpoints to ensure continuous execution without loss of context.*

---

## 1. Problem Statement & Context
- **Hackathon Track:** Data Science (8-Hour Time Budget)
- **Problem Statement:** *Pending Problem Statement from Organizers*
- **Organizer Constraints:** *Pending Organizer Materials*

---

## 2. Verified Data Sources
*(Will be updated once dataset is vetted and downloaded into `data/`)*
- Sourcing Standard: Genuine, recent, official/institutional only. Zero synthetic data.

---

## 3. Technology Choices & Justification
- **Frontend:** React (Vite) + Tailwind CSS + Lucide Icons + Recharts / Plotly. (Fast, lightweight, offline-ready).
- **Backend:** FastAPI + Uvicorn + Pydantic. (Async Python, typed validation, instant local execution).
- **Data & ML:** pandas, NumPy, scikit-learn / LightGBM, SHAP. (High tabular accuracy, fast offline inference, mathematical explainability).
- **UI Design:** Google Stitch (https://stitch.withgoogle.com/) for visual system; 45-min strict timebox.
- **Review System:** Google Elephant-Goldfish Model (EGM) subagents (`egm-design`, `egm-implementation-readiness`, etc.).

---

## 4. Key Architecture & Design Decisions
- **Offline-First:** All data, models, and assets stored locally in repository. Zero external dependencies required during demo.
- **Pre-Implementation Approval Gate:** No code written until 22-point plan passes EGM review and is explicitly approved by the user.

---

## 5. EGM Review Findings & Resolutions
*(To be recorded after Phase 2 EGM review)*

---

## 6. Failed Approaches & Learnings
*(To be logged as encountered to avoid repeating mistakes)*

---

## 7. Working Checkpoints & Commands
- **Python Environment:** Python 3.15.0, pip 26.2.1
- **Node Environment:** Node v26.12.0, npm 12.2.2
- **Quickstart Command (Target):** `./run.sh`

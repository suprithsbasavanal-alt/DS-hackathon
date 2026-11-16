# System Architecture Document (`architecture.md`)

*Status: Initial Architecture Blueprint — Awaiting Problem Statement*

---

## 1. System Overview
A high-performance, offline-capable Data Science web application designed for instant local execution, explainable inference, and responsive user interaction.

```
+-------------------------------------------------------------------------+
|                              USER BROWSER                               |
|   React (Vite) + Tailwind CSS + Lucide Icons + Recharts / Plotly        |
+------------------------------------+------------------------------------+
                                     |  HTTP REST (JSON) / Localhost:8000
                                     v
+-------------------------------------------------------------------------+
|                           BACKEND SERVICE                               |
|                FastAPI + Pydantic (Async Python Server)                 |
+------------------+----------------------------------+-------------------+
                   |                                  |
                   v                                  v
+----------------------------------+  +----------------------------------+
|      DATA PROCESSING PIPELINE    |  |       ML & INFERENCE ENGINE      |
|    pandas / NumPy / Polars       |  |  scikit-learn / LightGBM / SHAP  |
|   - Local cached CSV/Parquet     |  |  - Pretrained / Serialized Model |
|   - Reproducible preprocessing   |  |  - Instant offline prediction    |
|   - Zero data leakage            |  |  - Mathematically sound SHAP     |
+----------------------------------+  +----------------------------------+
```

---

## 2. Component Responsibilities
- **Frontend (`frontend/`)**: Modern React interface. Provides real-data KPI cards, interactive charts, scenario simulator controls, and responsive layouts.
- **Backend API (`backend/`)**: FastAPI service. Exposes typed REST endpoints for health check, dataset queries, model inference, and explainability attributions.
- **Data Ingestion (`data/`)**: Local storage of raw and cleaned real datasets. No synthetic or invented records.
- **Intelligence Pipeline (`backend/ml/` or `notebooks/`)**: Reproducible training script, validation harness, and serialized model artifacts (`.joblib` / `.pkl`).

---

## 3. Offline Execution Architecture
- All datasets stored locally in `data/`.
- All models serialized to local disk.
- Zero mandatory external API calls required for the core user journey.
- Startup script (`run.sh`) boots both backend and frontend locally with one command.

---

## 4. Security & Input Validation
- All inputs validated via Pydantic schemas.
- Out-of-bounds input protection.
- No exposed credentials; `.env` git-ignored.

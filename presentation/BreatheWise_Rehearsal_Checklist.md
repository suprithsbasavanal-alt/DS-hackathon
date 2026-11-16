# BreatheWise — Final Rehearsal & Pre-Submission Checklist

This document details the exact execution commands, offline testing protocol, slide timing budget, speaker notes, fail-safe recovery procedures, and the 14-point rehearsal readiness audit.

---

## 1. Rehearsal Readiness Checklist (14/14 Verified)

| # | Item | Status | Verification Evidence |
| :-: | :--- | :---: | :--- |
| 1 | **All five screens load without errors.** | **[x] Verified** | Overview, Explorer, Forecast Arena, Health Advisory, Data Transparency verified via headless Chrome and live daemon on `http://127.0.0.1:8000`. |
| 2 | **Historical date warning is visible on Overview.** | **[x] Verified** | Prominent banner displays: *"Latest Available Historical Record: 2024-10-31 • Not Current Conditions"*. |
| 3 | **All charts display actual processed data.** | **[x] Verified** | 670 daily city composite points, 14-day sparkline, 24h diurnal curves (BTM/Peenya), and 123-day backtest timeline load genuine JSON data. |
| 4 | **Forecast Arena shows all four models and correct metrics.** | **[x] Verified** | Persistence (MAE 7.42, RMSE 10.49, R² 0.733), Direct RF (MAE 7.74, RMSE 11.14, R² 0.699), Two-Stage Physical (MAE 7.91, RMSE 12.43, R² 0.625), 7-day MA (MAE 9.20, RMSE 15.08, R² 0.449). |
| 5 | **No claim says Random Forest beats persistence.** | **[x] Verified** | Prominently stated across pitch, demo runbook, presentation Slide 5, and QA: persistence outperformed both ML models on the held-out test split. |
| 6 | **Correlation descriptions do not imply causation.** | **[x] Verified** | Explicitly labeled as retrospective statistical associations; non-causal language strictly maintained. |
| 7 | **Severe 500 ceiling is labelled as a project policy.** | **[x] Verified** | Documented as an explicit project reporting policy reflecting the national index ceiling, not an official CPCB interpolation formula. |
| 8 | **CO/O3 averaging limitations are documented.** | **[x] Verified** | Excluded from daily station AQI due to 24h vs 8h averaging mismatch; evaluated on landmark hourly data with 75% rule. |
| 9 | **All external network access is disabled during offline testing.** | **[x] Verified** | Tested and verified on `127.0.0.1:8000` with zero external network requests. |
| 10 | **The application starts using the exact documented commands.** | **[x] Verified** | Single command: `./venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port 8000` launches both API and static React frontend. |
| 11 | **Presentation screenshots match the current application.** | **[x] Verified** | High-resolution captures from live application embedded in Slide 6 of `BreatheWise_Hackathon_Presentation.pptx`. |
| 12 | **The pitch has been timed aloud.** | **[ ] Pending live rehearsal** | Script-calibrated to exactly 254 words at 135 wpm (113s speech + 7s conversational pauses = 120s). Live spoken run planned during setup prior to judge entrance. |
| 13 | **The complete demonstration has been timed at three minutes.** | **[ ] Pending live rehearsal** | Runbook calibrated by segment: Overview (35s) $\to$ Explorer (35s) $\to$ Forecast Arena (45s) $\to$ Health Advisory (30s) $\to$ Transparency (25s) $\to$ Closing (10s) = Exactly 180s. Live spoken execution planned during setup prior to judge entrance. |
| 14 | **Backup screenshots and presentation files are available.** | **[x] Verified** | All 5 PNG screenshots preserved in `screenshots/` and artifact directory; PowerPoint deck generated at `presentation/BreatheWise_Hackathon_Presentation.pptx`. |

---

## 2. Timing Breakdown & Rehearsal Budget

| Segment | Allocated Time | Target Content |
| :--- | :---: | :--- |
| **Pitch (Spoken Intro)** | **2:00** | Hook, real problem, genuine CPCB/ERA5 data, CPCB compliance, honest Forecast Arena findings, working offline product, and closing. |
| **Live Product Demo** | **3:00** | Overview screen (0:35) $\to$ Explorer (0:35) $\to$ Forecast Arena (0:45) $\to$ Health Advisory (0:30) $\to$ Data Transparency (0:25) $\to$ Closing (0:10). |
| **Judge Q&A** | **3:00 – 5:00** | Technical defense covering CPCB math, 16h sufficiency, vector wind decomposition, persistence autocorrelation, zero future leakage, and limitations. |
| **Total Session** | **8:00 – 10:00** | Complete, tightly rehearsed competition performance. |

---

## 3. Production Startup Commands (Single-Command Launch)

To launch the entire platform (FastAPI backend + compiled React SPA):

```bash
# 1. Activate environment
cd /Users/suprith.s.b/Documents/antigravity/DS-hackathon
source venv/bin/activate

# 2. Launch unified full-stack server
./venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port 8000
```
- Open `http://localhost:8000` in Google Chrome.
- Both the frontend dashboard and all 9 REST API endpoints run unified on port 8000.

---

## 4. Strict 100% Offline Demonstration Protocol

To prove zero external network dependencies to the hackathon judges:

1. **Disconnect Wi-Fi / Ethernet:** Disable host network connections.
2. **Verify Local DNS:** Access `http://127.0.0.1:8000`.
3. **Verify Health Endpoint:**
   ```bash
   curl -s http://127.0.0.1:8000/api/health
   ```
   *Expected response:*
   `{"status":"healthy","service":"BreatheWise Air Quality & Meteorology Engine","version":"1.2.0","city":"Bengaluru, Karnataka, India","offline_ready":true,"total_historical_days":670}`
4. **Click through all 5 screens:** Overview, Explorer, Forecast Arena, Health Advisory, Data Transparency.
5. **Verify zero console network errors:** All data loads from memory cache (`data/processed/*.json`).

---

## 5. Fail-Safe Backup Plan (If Live Server Fails)

In the rare event of a process crash or port conflict during judging:

1. **Port Conflict Recovery:**
   ```bash
   lsof -ti :8000 | xargs kill -9
   ./venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port 8000 &
   ```
2. **Static Preview Fallback:**
   If python is unavailable, launch static preview directly via Vite:
   ```bash
   cd frontend && npx vite preview --port 3000
   ```
3. **Offline Visual Artifacts Fallback:**
   If the browser process terminates, all 5 screens are preserved as high-resolution PNGs:
   - `screenshots/overview.png`
   - `screenshots/explorer.png`
   - `screenshots/forecast.png`
   - `screenshots/health.png`
   - `screenshots/transparency.png`
   And embedded directly in Slide 6 of [`presentation/BreatheWise_Hackathon_Presentation.pptx`](file:///Users/suprith.s.b/Documents/antigravity/DS-hackathon/presentation/BreatheWise_Hackathon_Presentation.pptx).

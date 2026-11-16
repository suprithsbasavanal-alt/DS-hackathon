# UI/UX & Design System (`design.md`)

*Single Source of Truth for Visual Direction, Google Stitch Integration, and Component Tokens*

---

## 1. Product Visual Direction
- **Brand Aesthetic:** Professional, startup-grade, data-dense yet clean and accessible.
- **Tone:** Authoritative, scientific, trustworthy, and modern.
- **Theme:** Dark mode default with crisp high-contrast elements (slate/zinc palette).

---

## 2. Color System & Tokens
- **Canvas / Background:** Deep Slate (`bg-slate-950` / `#020617`, secondary `bg-slate-900` / `#0f172a`)
- **Card Surfaces:** Elevated cards with 1px border (`bg-slate-900/70`, `border-slate-800`, backdrop-blur)
- **Primary Brand Accent:** Electric Blue / Indigo (`#3b82f6` / `#6366f1`) for core CTAs and primary metrics
- **Insight / Positive Accent:** Emerald Green (`#10b981`) for positive trends, high confidence, safe states
- **Warning / Alert Accent:** Amber / Rose (`#f59e0b` / `#f43f5e`) for critical thresholds, high risk, anomalies
- **Typography Colors:** `#f8fafc` (headers/primary), `#94a3b8` (body/labels), `#64748b` (subtle captions)

---

## 3. Typography & Spacing
- **Font Family:** Inter / Geist Sans (sans-serif)
- **Scale:**
  - Page Title: `text-2xl md:text-3xl font-bold tracking-tight`
  - Section Header: `text-lg font-semibold text-slate-100`
  - KPI Stat: `text-3xl font-extrabold font-mono tracking-tight`
  - Labels & Body: `text-sm text-slate-400`
  - Tooltips & Badges: `text-xs font-medium`

---

## 4. Screen Layouts & Component Standards
1. **Header Navigation:** App title, status badge ("Offline-Ready / Verified Data"), live clock, quick reset.
2. **Top KPI Strip:** 4 cards highlighting key numbers directly from the real dataset.
3. **Core Interactive Zone:**
   - Left: Parameter controls / scenario sliders.
   - Right: Live prediction gauge, confidence meter, and SHAP feature attribution bar chart.
4. **Data Visualization Hub:** High-contrast Recharts/Plotly charts with plain-language takeaway under each chart.
5. **Trust & Provenance Drawer:** Dataset citation, observation dates, row counts, and data license.

---

## 5. Google Stitch Integration
- Official tool: [https://stitch.withgoogle.com/](https://stitch.withgoogle.com/)
- Initial design timebox: **Strict 45-minute cap**.
- Focus: Dashboard, scenario simulator, results screen, input panel.
- Handoff: Adapt Stitch design tokens and screen layouts into modular React/Tailwind components.

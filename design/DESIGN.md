# Google Stitch Integration & Design System (`design/DESIGN.md`)

This document serves as the single source of truth for the visual design system established with Google Stitch.

---

## 1. Visual Direction & Brand Identity
- **Product Name:** *Pending Problem Statement*
- **Aesthetic:** Minimalist, high-contrast, startup-grade, data-dense yet clean.
- **Tone:** Authoritative, scientific, trustworthy, modern.

---

## 2. Color Palette & Tokens
- **Background:** Clean neutral slate/zinc (`bg-slate-950` / `bg-slate-900` dark; `bg-slate-50` light)
- **Surfaces / Cards:** Layered elevation with subtle 1px border (`border-slate-800`, `bg-slate-900/60`, backdrop-blur)
- **Primary Accent:** Electric Indigo / Vivid Blue (`#3b82f6` / `#6366f1`) for primary actions and key data series
- **Secondary Accent:** Emerald / Cyan (`#10b981` / `#06b6d4`) for positive insights, high confidence, and confirmation states
- **Alert / Warning:** Amber / Rose (`#f59e0b` / `#f43f5e`) for critical thresholds, risks, and anomaly flags
- **Text:** High contrast white/off-white (`#f8fafc`) for headers, muted slate (`#94a3b8`) for secondary text

---

## 3. Typography
- **Font Family:** Inter / Geist Sans (sans-serif)
- **Scale:**
  - Page Titles: `text-2xl` to `text-3xl font-bold tracking-tight`
  - Card Headers: `text-base font-semibold`
  - KPI Metrics: `text-3xl font-extrabold font-mono tracking-tight`
  - Body / Labels: `text-sm text-slate-400`
  - Tooltips & Footers: `text-xs text-slate-500`

---

## 4. Component Hierarchy & UX Rules
1. **Header / Hero Bar:** Brand logo, live dataset badge ("Real-time / Verified Gov Source"), status pill, and quick navigation.
2. **KPI Highlights:** Top row 4-card metric strip showing core dataset dimensions, baseline benchmark, model accuracy, and active filter counts.
3. **Primary Interactive Workspace:**
   - Left Column: Interactive Scenario Inputs & What-If controls.
   - Right Column: Live Prediction Gauge, SHAP Explanations, and Confidence Interval.
4. **Data Exploration & Visualizations:** Interactive charts (Recharts) with plain-language takeaway callouts underneath each figure.
5. **Trust & Methodology Panel:** Drawer/footer showing data provenance, preprocessing steps, and citation links.

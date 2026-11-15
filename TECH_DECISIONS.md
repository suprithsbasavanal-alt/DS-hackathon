# Technical Decisions & Architecture Justifications

Every major technical choice is justified in one line below:

| Layer | Technology | Decision Justification | Status |
| :--- | :--- | :--- | :--- |
| **Data Processing** | Python, pandas, NumPy | Industry standard, high reliability, robust handling of real-world tabular data. | Approved |
| **Modelling** | scikit-learn / LightGBM / XGBoost | Fast training, high tabular accuracy, reliable serialization, and instant inference. | Approved |
| **Explainability** | SHAP (Tree/KernelExplainer) | Provides mathematically grounded feature importance and local decision transparency for judges. | Approved |
| **Backend API** | FastAPI + Uvicorn | Async Python speed, automatic OpenAPI/Swagger docs, native Pydantic validation. | Approved |
| **Frontend** | React (Vite) + Tailwind CSS + Lucide Icons + Recharts | Lightning-fast build times, zero latency dev server, clean modern responsive UI. | Approved |
| **Data Visuals** | Recharts / Plotly | Interactive, accessible, and supports tooltips, legends, and KPI representations. | Approved |
| **Design & UI/UX** | Google Stitch + Tailwind CSS | AI-powered UI design partner for high-fidelity layouts, DESIGN.md specs, component tokens, and startup-grade visual polish. | Approved |
| **Presentation** | Markdown Pitch Deck + Demo Script | Reproducible, version-controlled, and instantly exportable to slides/PDF. | Approved |

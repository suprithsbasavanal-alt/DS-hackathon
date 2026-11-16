# BreatheWise --- Execution Phase Tracker

**Hackathon plan:** 8 hours\
**Current state:** Pre-implementation gates\
**Project approval:** Approved by Suprith\
**Implementation:** NOT STARTED

## Status legend

-   NOT STARTED
-   IN PROGRESS
-   BLOCKED
-   COMPLETED

Only mark a task COMPLETED after checking its acceptance evidence.

## Phase 0 --- Organizer compliance

**Status:** IN PROGRESS

Reported by team: - AI tools allowed. - External APIs allowed. -
Datasets allowed. - Prebuilt code allowed. - External development tools
allowed. - Team maximum: four. - Active builders: Suprith and Uday.

Still confirm: - Submission format and deadline. - Judging criteria. -
Demo/presentation duration. - Deployment requirement. -
Repository/submission rules. - Team registration and contribution rules.

## Phase 1 --- Data research and verification

**Status:** IN PROGRESS

Candidates: - Peenya CPCB 15-minute 2024--25 CSV via OpenCity. - OpenAQ
Jayanagar 5th Block historical station. - Open-Meteo historical weather,
if needed.

Pending: - Download actual CSV. - Inspect row count and real date
coverage. - Inspect all actual columns and dtypes. - Validate
timestamps/time zone and sampling intervals. - Calculate missingness and
duplicates. - Check invalid/outlier/flatline values. - Verify units and
station. - Confirm source attribution/licence. - Decide whether the
dataset supports a valid PM2.5 forecast.

Do not begin model training before this phase is complete.

## Phase 2 --- Final specification and review

**Status:** IN PROGRESS

-   PRD drafted.
-   Architecture drafted.
-   Design specification drafted.
-   Permanent rules drafted.
-   Independent EGM review not performed; capability not
    available/verified in current assistant tools.
-   Transparent manual technical review performed in conversation; this
    is not an EGM review.
-   Final implementation approval remains conditional on data and
    compliance gates.

## Phase 3 --- Stitch design

**Status:** NOT STARTED

-   Overview screen.
-   Explorer screen.
-   Forecast screen.
-   Weather Relationships.
-   Insights.
-   Final design system and responsive rules.

## Phase 4 --- MVP vertical slice

**Status:** NOT STARTED

Acceptance: - Real data loads. - One end-to-end analysis is visible in
UI. - Source/time/unit labels are correct. - Core workflow runs locally.

## Phase 5 --- Core integration

**Status:** NOT STARTED

-   Explorer filters work.
-   Weather relationship chart works.
-   Summary statistics are reproducible.
-   Backend/frontend integration passes.

## Phase 6 --- Distinctive feature and polish

**Status:** NOT STARTED

-   Forecast and explanation only if data/model passes.
-   Anomaly detection with documented method.
-   Pollution Pattern Explainer based on actual evidence.
-   UI polish.

## Phase 7 --- Testing and offline readiness

**Status:** NOT STARTED

-   Test core workflow with network disabled.
-   Test missing data and invalid filters.
-   Test API failure and cache fallback.
-   Check charts and timestamps.
-   Resolve critical bugs.
-   Save backup demo recording.

## Phase 8 --- Presentation and submission

**Status:** NOT STARTED

-   README complete.
-   PITCH complete.
-   Slides complete.
-   Architecture/data-flow diagram.
-   Honest metrics and limitations.
-   Demo click-path rehearsed.
-   Submission package checked.

## Current blockers

1.  Actual dataset file not yet uploaded/inspected.
2.  Remaining organizer submission/judging details unknown.
3.  Forecast horizon and model cannot be locked until data inspection.

## Next action

Obtain the actual Peenya CSV (or retrieve OpenAQ data) and inspect it.
Ask organizers/teacher for submission format and judging criteria. Keep
implementation paused until the data gate is satisfied.

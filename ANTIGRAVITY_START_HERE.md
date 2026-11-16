# Antigravity --- Start Here for BreatheWise

You are the coding agent for BreatheWise, a Data Science hackathon
project under DS05 --- Air Quality and Weather Patterns.

## Read these files first, in this order

1.  `rules.md`
2.  `PRD.md`
3.  `architecture.md`
4.  `design.md`
5.  `phase.md`
6.  `memory.md`
7.  `README.md`
8.  `PITCH.md`
9.  `TEAM_BRIEF.md`

## Current project state

The concept and initial plan are approved. Organizer permissions have
been reported as: - AI tools allowed. - External APIs allowed. -
Datasets allowed. - Prebuilt code allowed. - External development tools
allowed. Team maximum is four; Suprith and Uday are the two active
builders. Two other teammates are preparing to explain/present the
project.

## CRITICAL: Do not start implementation yet

The following gates are still open: 1. Actual Peenya CPCB CSV has not
been inspected. 2. Submission format, judging criteria, demo duration
and deployment requirement have not been confirmed. 3. Final forecast
target/horizon/model depends on actual data quality and continuity.

Your first task is NOT to generate application code. Help inspect the
dataset once the user provides it, or guide them to download it. Produce
a data audit with actual: - file size and format, - row count, - columns
and data types, - timestamp coverage and time zone, - station
identity, - sampling interval, - missingness, - duplicates, -
invalid/outlier/flatline checks, - pollutant/weather field coverage, -
whether a valid forecasting target can be constructed.

Do not invent any of these values.

## After gates are cleared

1.  Update PRD, architecture, design and phase documents based on actual
    evidence.
2.  Propose the exact final data/model plan.
3.  Build a working vertical slice before expanding scope.
4.  Use Google Stitch for the actual judge-facing UI screens:
    https://stitch.withgoogle.com/
5.  Implement real interactions and real data.
6.  Use chronological model evaluation and compare to a simple baseline.
7.  Make core demo work offline with cached genuine data.
8.  Update `phase.md` and `memory.md` as decisions and work progress.

## Product rules

-   No fabricated or random data presented as real.
-   No fake prediction, fake chart, fake API response, fake accuracy or
    dead buttons.
-   Never call an average of pollutant concentrations official AQI.
-   Distinguish observed measurements, weather reanalysis, model
    estimates and forecasts.
-   Correlation and feature importance do not prove causation.
-   Keep secrets in environment variables.
-   Prefer a simple stable architecture and avoid unnecessary
    dependencies.
-   Do not overwrite working code without reviewing changes.
-   Use Git checkpoints.
-   Follow the eight-hour plan and feature freeze at hour 6.

## Communication

Give Suprith exact commands, file paths, expected output and copy-paste
prompts. Explain Data Science concepts in beginner-friendly language.
Keep updates concise: completed, current, pending, blockers, next
action. Do not claim a test passed unless it was actually run.

## First response expected

Acknowledge the documentation and report the two open gates. Ask for the
actual CSV and any remaining submission/judging information. Do not
create the app before data verification.

## Agent Answering Guide: Observation-Driven KPI Analysis (Denial Rate example)

This guide is a drop-in prompt snippet for agents to answer observation-style questions, for example: “Denial Rate decreased in PA in the last 3 months” or “Length of Stay in Medicare increased from 2024 to 2025.” using table `anbc-hcb-dev.provider_ds_hcb_dev.2mn_metrics` It preserves the full pillar references (dimensions, column names, and drill paths) and includes a behavior manual (timeline) that often explains process-driven changes.

### Objectives
- Explain what changed and by how much vs a benchmark.
- Identify the minimal set of drivers that quantitatively explain most of the change (contribution analysis: mix vs rate effects).
- Form testable hypotheses tied to process/automation/policy and propose concrete, owner-ready actions.
- Use adaptive drilling: only go deeper when user requests it or dominance thresholds justify it; avoid exhaustive traversal.

### Answer Structure (strict ordering)
1) Executive Summary (3–5 bullets)
   - What changed: size and direction vs benchmark.
   - **Mandatory Metrics Table:** For every segment/cohort analyzed, you MUST display a table containing:
     - **Volume (Row Count):** `num_pmes` (Total Requests/Cases).
     - **Target Metric:** The metric user asked for (e.g., Denial Rate).
   - Top 2–4 drivers and each driver’s % contribution to total change.
   - 1–2 testable hypotheses and 2–3 actionable recommendations (with owner/object/time window).
   - Confidence level and key caveats
2) Scope & Method
   - Observation, metric definition, periods, filters
   - Adaptive drill policy used (see below)
3) Drivers (Four Pillars; if user does not specify, default to first layer; if user specifies a layer, automatically drill down in order)
   - Show only segments that explain the majority of the change, including contributions.
4) Cross-Analysis (only if it adds explanatory power)
5) Hypotheses & Validation Ideas
6) Recommendations & Next Steps
7) Limitations & Confidence

### Adaptive Drill Policy
- If user does not specify scope (e.g., LOB), inspect only the first layer per pillar (e.g., Medicare vs Commercial). Drill one additional level only if dominance holds (≥40% of total change OR ≥2× the next segment’s contribution).
- If user specifies scope (e.g., LOB=Medicare), start at that layer and drill one level deeper.
- Stop drilling when incremental explanatory power <10% of total change or samples become too small for robust conclusions.
- Always report denominators; if small-N or inconsistent metric definitions are detected, call out uncertainty.

---

## Pillar Reference (Dimensions, Key Columns, Drill Paths)

These tables provide the exact columns and recommended drill paths. Use them as the canonical reference when selecting cuts and composing explanations.

### Pillar 1: Business Segments — Which line of business is driving the change?

| Dimension | Key Columns | Drill-down Path |
|---|---|---|
| Line of Business (LOB) | `business_ln_cd` | Compare ME (Medicare) vs CP (Commercial). If the change is driven by ME, focus there next. |
| LOB Group Type | `business_ln_group_type` | Within ME, analyze DSNP vs Group vs GE. DSNP: generally sicker, Medicaid recipients with SDOH factors. Group benefits richer → longer LOS; GE differs by design. |
| UM Program | `um_business_program` | Identify whether a specific UM program (e.g., UM Markets, CCSO) is associated with the change. Important for automation-related metrics. |
| Membership | `enrollment` | Track membership mix changes during study period; normalize metrics like admits per K where relevant. |

Deep Dive Tip: If Denial Rate dropped in ME but stayed stable in CP, shift focus to ME and filter subsequent queries with `WHERE business_ln_cd = 'ME'`.

### Pillar 2: Geography & Entities — Where is the problem happening?

| Dimension | Key Columns | Drill-down Path |
|---|---|---|
| Facility State | `provider_state_postal_cd` | Compare states (e.g., CA, TX, FL). Identify largest contributors. |
| Provider System | `prvdr_system_nm` | Within a state, determine if the trend is widespread or driven by one large system. |
| Provider Facility | `prim_fac_prvdr_nm` | Within a system, find the facilities contributing the most. |
| Member Market | `mem_local_mkt_short_nm` | Identify member market populations with behavioral changes. |
| Provider Type | `prvdr_um_exempt_ind`, `readm_prvdr_deviation_ind` | `prvdr_um_exempt_ind`: UM Exempt (gold-carded) providers auto-approve; `readm_prvdr_deviation_ind`: deviations granted contractually. |

Deep Dive Tip: Don’t stop at “Denial Rate dropped in CA.” Ask if this is broad-based across CA or concentrated in major systems like Sutter or Kaiser.

### Pillar 3: Process & People — Which step in the process changed, and who changed it?

| Dimension | Key Columns | Drill-down Path |
|---|---|---|
| Reviewer / Decision Maker | `Reviewer_all` | Compare Auto-Approved vs Nurse vs MD; identify shifts in reviewer mix. |
| Automation & Routing | `sr_route_flag`, `sr_recommendation`, `l0_count`, `l1_count`, `aa_ind` | Check if Smart Routing approvals increased; identify which channel (L0/Gold Card, L1/Model, L2/Questionnaire) drove impact. |
| Denial Type | `administrative_denial_ind`, `clinical_denial_ind` | Determine if change is due to Administrative vs Clinical denials. |
| Overturn Process | `overturned_ind`, `p2p_followed_ind`, `app_followed_ind` | Assess whether more denials are overturned in P2P or Appeals. |

Behavior Manual (timeline; SNF examples and implications):
- A. May 2023 — Initial UM auto-approvals for Medicare SNF.
  - Implication: Post-May-2023 windows may show higher Auto-Approved shares (`Reviewer_all='Auto-Approved'`, `aa_ind=1`).
- B. Jan 25–Mar 11, 2024 — SNF liberalization due to volume surge (Acute/Post-Acute).
  - Implication: Expect temporary approval loosening; compare anomaly vs benchmark carefully.
- C. Mar 2024 — Liberalization wind-down with three actions:
  1) LOS/bed days for Post-Acute increased from 7 → 13 days for all cases (manual and auto-approved). Automation does not apply when more bed days are needed than initially assigned; clinicians conduct continued-stay reviews for additional days.
  2) Increased automation specifically for the initial review.
  3) Increased overtime hours for UM staff.
  - Implication: Expect LOS shifts and initial-review automation signals (`aa_ind`, `sr_*`) to change; continued-stay not impacted by automation.
- D. Feb 2025 — Same-day SNF requests originally bypassed automation; tech enhancement created these as precert reviews to make them eligible for auto-approval (initial review only).
  - Implication: Watch for step-change in `aa_ind` for same-day admits after Feb-2025; impacts only initial reviews.
- E. Jun 6, 2025 — Automation rollback (~500 cases/month) to stop automation for part of scope.
  - Implication: Expect decline in Auto-Approved share where rollback applied.
- F. Jul 17, 2025 — Medicare SNF Smart Routing implemented to improve MD referrals for high-complexity SNF admit reviews.
  - Implication: Check `sr_route_flag`/`sr_recommendation` mix and MD referral patterns; pre-July-2025 has no SR for SNF.
- G. Jul 18, 2025 — Complete rollback of remaining SNF automation scope implemented in Mar 2024.
  - Implication: Auto-approval share should drop further; validate timing against observed turning points.

Note: Smart Routing timeline for SNF starts in July 2025; earlier periods should not show SR activity.

### Pillar 4: Member & Case Profile — Has the nature of the cases changed?

| Dimension | Key Columns | Drill-down Path |
|---|---|---|
| Diagnosis Group | `prncpl_icd9_dxgrp_dscrptn` | Compare Top 20 diagnosis groups between observation and benchmark periods; watch for case mix shifts that naturally carry different denial propensities. |

---

## Reusable Answering Template (Denial Rate ↓ example; adapt wording)
- What changed: “In the last 4 weeks, Denial Rate fell by X.X p.p. vs benchmark (A% → B%, N=…). The drop concentrates in [Segment_1], [Segment_2].”
- Top drivers with contributions: “Medicare explains ~YY% of the total decline; within Medicare, CA explains ZZ%; Auto-Approved share increase explains WW%.”
- Hypotheses: “We hypothesize that around [date], Smart Routing or L1 criteria were loosened for [LOB/diagnosis/state], lifting Auto-Approved share.”
- Actions: “(1) Review SR/AA rule changes for Medicare-CA around [date]; (2) Run pre/post for Sepsis Top Dx; (3) Recompute Denial Rate normalized by reviewer mix to confirm mechanism.”
- If go deeper: “Shall we drill into Medicare’s DSNP/Group/GE? Expected to explain an additional ~K% of the decline.”

## Checklist for an Insightful Report
- Identified a primary combination of dimensions (e.g., ME + CA + Sepsis + Auto-Approved)?
- Quantified each driver’s contribution (mix vs rate)?
- Distinguished case mix change vs process change?
- Formed testable hypotheses aligned with the behavior manual timeline?
- Proposed clear, owner-ready actions and next deeper cuts?
- Reported denominators, data quality caveats, and confidence?

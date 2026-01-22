# REPORT TEMPLATE SPECIFICATION
## Billboard-style Soccer Player Rankings App — Product De-risking Research

**Status:** Authoritative  
**Audience:** Engineering, Agent authors, PM  
**Purpose:** Define the ONLY acceptable output structure for market research reports

---

## 0. Problem Statement

The research system must produce a **product decision memo**, not a descriptive analytics report.

The report must explicitly answer:
1. What moment should the app own?
2. How must rankings earn trust?
3. What gets shared to drive growth?
4. Who is V1 for?
5. What must NOT be built?

Any report that does not answer these questions explicitly is **invalid**.

---

## 1. Non-Negotiable Principles

- Research is organized by **Research Questions (RQ1–RQ5)**, not by segments or themes
- Each RQ must include:
  - A decision-oriented table
  - A written decision statement
- Aggregate analytics sections (e.g., “Segment Analysis”) are forbidden unless embedded in an RQ
- The output is evaluated on **decision clarity**, not data volume

---

## 2. Required Research Questions

### RQ1 — Where do fans already go during the moments we want to own?
**Decision unlocked:** Primary habit moment

### RQ2 — What makes rankings feel credible vs annoying?
**Decision unlocked:** Trust + explainability requirements

### RQ3 — What content do fans actually share?
**Decision unlocked:** Share artifact / growth loop

### RQ4 — Which segment should V1 optimize for?
**Decision unlocked:** V1 wedge segment

### RQ5 — What causes churn even if users like rankings?
**Decision unlocked:** Do-not-build list

---

## 3. Required Report Structure

The report MUST follow this order:

1. Executive Summary (decisions only)
2. Data Collection Overview (scope + coverage)
3. RQ1 section
4. RQ2 section
5. RQ3 section
6. RQ4 section
7. RQ5 section
8. V1 Product Blueprint
9. Appendix (evidence + QA)

---

## 4. Required RQ Section Format (Template)

Each RQ section MUST include the following blocks, in order.

### 4.1 Decision Context
One sentence explaining what product decision this RQ unlocks.

### 4.2 Decision Table (MANDATORY)

Each RQ has its own table schema.  
If the table is missing or empty → **FAIL**

Example (RQ1):

| Moment | Platform(s) today | Content type | Player-centric? | Ranking-like? | Product implication |
|------|------------------|--------------|-----------------|---------------|---------------------|

### 4.3 Findings
3–7 bullet points summarizing what the evidence shows.

### 4.4 Decision Statement (MANDATORY)
A single, opinionated product decision written in plain English.

### 4.5 Confidence and Open Risks
- Confidence: High / Medium / Low
- Known uncertainties

### 4.6 Evidence Snapshot
Top 6 deduplicated evidence items supporting the decision.

---

## 5. Executive Summary Requirements

The Executive Summary MUST contain these five explicit decisions:

- Primary habit moment
- Trust model
- Share artifact
- V1 wedge segment
- Do-not-build list

If any are missing → **FAIL**

---

## 6. V1 Product Blueprint (MANDATORY)

### 6.1 Core Loop
Numbered steps describing the user journey.

### 6.2 Surfaces & Mechanics Table

| Surface | Primary mechanic | Target segment | Rationale |
|--------|------------------|----------------|-----------|

### 6.3 Do-not-build List
Explicit list of features or patterns to avoid in V1.

---

## 7. Forbidden Patterns (Automatic Failure)

The report MUST FAIL validation if any of the following appear:

- “General” as a segment, theme, job, or moment
- “General Inquiry” as a job-to-be-done
- Sections titled:
  - Segment Analysis
  - Theme Analysis
  - Jobs-to-be-Done (outside RQs)
- Duplicate top evidence (similarity > 0.85)
- No decision tables
- No decision statements

---

## 8. Validation Checklist (Engineering)

Before rendering a report:
- [ ] All RQs present (1–5)
- [ ] Each RQ has a populated decision table
- [ ] Each RQ has a decision statement
- [ ] Executive summary lists 5 decisions
- [ ] V1 Product Blueprint present
- [ ] No forbidden patterns detected

---

## 9. Definition of Done

A report is “done” only if a PM can answer, without inference:

> “What should we build, for whom, when, and why?”

If not, the output is invalid.

---
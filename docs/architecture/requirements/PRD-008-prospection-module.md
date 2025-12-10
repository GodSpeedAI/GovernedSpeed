# PRD-008: Prospection & Innovation Module

**Version:** 1.0  
**Date:** 2025-12-09  
**Author:** Architecture Team  
**Status:** Draft

---

## 1. Overview

This document defines the product requirements for the **Prospection & Innovation Module** — the system components responsible for anticipating future risks, allocating resources across strategic horizons, and enabling the "Evolutionary Engine."

### 1.1 Problem Statement

Most governance systems are reactive — they enforce rules about the present, but don't help organizations anticipate the future. As a result, strategic pivots are slow and painful. This module provides foresight by:

1.  Continuously sensing market and operational signals.
2.  Dynamically allocating exploration budgets (H1/H2/H3).
3.  Automating the feedback loop that turns successful experiments into standard practice.

### 1.2 Goals

1.  **Foresight:** Provide early warning of market shifts and emerging risks.
2.  **Adaptive Allocation:** Automatically rebalance resources based on market velocity.
3.  **Learning Capture:** Encode successful human judgment into reusable playbooks.
4.  **Role Clarity:** Give each organizational layer the right view of the future.

---

## 2. Target Users

| Persona            | Horizon  | Needs                                                               |
| ------------------ | -------- | ------------------------------------------------------------------- |
| **Executive**      | H3 (5yr) | Strategic radar for existential threats, market disruption signals. |
| **Strategic (VP)** | H2 (2yr) | Capability gaps, competitor moves, new opportunity areas.           |
| **Tactical (Mgr)** | H1 (6mo) | Process optimization candidates, automation progress.               |
| **AI Agent**       | H1       | Data to identify successful discretionary patterns for promotion.   |

---

## 3. Functional Requirements

### 3.1 Sensing Layer

- **FR-1.1:** The module MUST continuously track **Market Velocity** (composite YoY change).
  - Data sources: Revenue trends, new entrant rate, tech adoption curves, regulatory changes.
- **FR-1.2:** The module MUST track **Automation Rate** across all H1 playbooks.
  - Formula: `Mandatory_Tasks / Total_Tasks`.
- **FR-1.3:** The module SHOULD provide a **Wardley Map Updater** agent that tracks component evolution from external signals (news, patents, academic research).
- **FR-1.4:** The module MUST produce a weekly `strategic_radar.json` report.

### 3.2 Allocation Engine (Fibonacci Budgeting)

- **FR-2.1:** The module MUST implement the **Fibonacci Exploration Ladder** algorithm.
  - Input: Current Market Velocity Gate (Stable, Moderate, Dynamic, Disruptive).
  - Output: Recommended % allocation for H1, H2, H3.
- **FR-2.2:** The module MUST run on a **quarterly cadence** (CronJob or scheduled workflow).
- **FR-2.3:** The module SHOULD support an **Event-Driven Override**: An executive can trigger an immediate budget reallocation.

### 3.3 Role-Stratified Dashboards

- **FR-3.1:** The module MUST provide dashboard views tailored to each persona:
  - **Executive Console:** 5-Year Strategic Radar, H3 case list.
  - **Strategic Dashboard:** 2-Year Opportunity Map, H2 experiment tracker.
  - **Tactical Board:** Quarterly Efficiency KPIs, Automation Rate trend.
- **FR-3.2:** Dashboard data MUST be sourced from the RES API.

### 3.4 Evolutionary Feedback Loop

- **FR-4.1:** AI agents MUST monitor for **Discretionary Plays** — instances where a human successfully deviated from the standard playbook.
- **FR-4.2:** Upon detecting a successful pattern (e.g., 3 consecutive successes), the agent MUST propose a **Policy Update** as a draft Pull Request to the `policies/` repo.
- **FR-4.3:** The PR MUST include:
  - The proposed new/updated policy rule (YAML).
  - Links to the evidence that supports the change.
  - A `GovernanceDelta` record summarizing the change.
- **FR-4.4:** The PR MUST require human approval before merge (no auto-merge).

---

## 4. Non-Functional Requirements

- **NFR-1:** Transparency: All budget recommendations MUST be explainable (show input data and formula).
- **NFR-2:** Latency: Dashboard views MUST load in < 3 seconds.
- **NFR-3:** Security: Sensing agents MUST NOT have write access to production systems.
- **NFR-4:** Auditability: All `GovernanceDelta` events MUST be stored in RES.

---

## 5. Data Model (Key Entities)

```typescript
// strategic_radar.json
interface StrategicRadar {
  timestamp: string;
  market_velocity: {
    composite_yoy_change: number; // e.g., 0.12 (12%)
    gate: "STABLE" | "MODERATE" | "DYNAMIC" | "DISRUPTIVE";
    factors: {
      revenue_change: number;
      new_entrant_rate: number;
      // ...
    };
  };
  allocation_recommendation: {
    h1: number; // e.g., 0.76
    h2: number; // e.g., 0.18
    h3: number; // e.g., 0.06
  };
  signals: SignalItem[]; // Array of detected weak signals
}

// GovernanceDelta (stored in RES)
interface GovernanceDelta {
  id: string;
  timestamp: string;
  before_policy_id: string | null;
  after_policy_id: string;
  change_type: "NEW_RULE" | "UPDATED_THRESHOLD" | "DEPRECATED_RULE";
  justification_evidence_ids: string[];
  approved_by: string;
}
```

---

## 6. Success Metrics (KPIs)

| KPI                             | Target                                                   |
| ------------------------------- | -------------------------------------------------------- |
| _Governance Delta Closure Rate_ | ≥ 90% of AI-proposed policy updates reviewed in 30 days. |
| _Policy Update Velocity_        | Average time from issue → merged policy ≤ 30 days.       |
| _Automation Rate (H1)_          | Target depends on domain (60-90%).                       |
| _Strategic Radar Accuracy_      | TBD (measure prediction vs. actual market events).       |

---

## 7. Dependencies

- [ADR-011: Prospection & Evolutionary Engine](../decisions/ADR-011-prospection-evolutionary-engine.md)
- [PRD-002: Risk & Evidence Service](./PRD-002-risk-evidence-service.md)
- [SDS-011: Sensing Layer](../specs/SDS-011-sensing-layer.md)

---

## 8. Open Questions

1.  What data sources for Market Velocity are available and reliable?
2.  How do we prevent "alert fatigue" from too many AI-proposed policy updates?
3.  What is the minimum evidence threshold to propose a policy change?

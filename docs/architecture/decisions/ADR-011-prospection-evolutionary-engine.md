# ADR-011: Prospection & Evolutionary Engine

**Status:** Accepted  
**Date:** 2025-12-09  
**Deciders:** Architecture Team, Governance Council, Executive Sponsor  
**Technical Story:** Define the architectural pattern for the "self-improving" governance system, implementing the Prospection Architecture and Constrained Evolution feedback loop.

---

## Context and Problem Statement

Beyond basic governance, the Governed Speed platform aims to be a _learning organization_. This requires mechanisms for:

1.  **Prospection:** Looking ahead at multiple time horizons (H1/H2/H3) to anticipate future risks and opportunities.
2.  **Evolution:** Continuously refining playbooks and policies based on operational feedback.

This ADR codifies the "Evolutionary Engine" formula:

> **Constrained Evolution = Guided Autonomy × Constrained Execution**

## Decision Drivers

- **Adaptability:** The system must learn faster than the market changes.
- **Risk Management:** Balance exploration (H2/H3) with exploitation (H1).
- **Human-in-the-Loop:** AI suggests, humans approve policy changes.
- **Auditability:** Evolution must be traceable for compliance.

## Decision Outcome

We will implement a **four-layer architecture** for the Evolutionary Engine:

### Layer 1: Sensing (Continuous)

- **Purpose:** Detect signals for change.
- **Components:**
  - **Market Velocity Agent:** Calculates YoY market change composite.
  - **Automation Rate Tracker:** Monitors `mandatory_tasks / total_tasks` ratio.
  - **Wardley Map Updater:** AI agent that tracks component evolution from external signals (news, patents).
- **Output:** `strategic_radar.json` — a weekly report of market signals.

### Layer 2: Allocation (Quarterly Cadence)

- **Purpose:** Allocate resources across Horizons using Fibonacci budgeting.
- **Algorithm (Fibonacci Exploration Ladder):**

  | Market Velocity (YoY) | H1 (Ops) | H2 (Strategic) | H3 (Transformational) |
  | --------------------- | -------- | -------------- | --------------------- |
  | Stable (<5%)          | 89%      | 8%             | 3%                    |
  | Moderate (5-15%)      | 76%      | 18%            | 6%                    |
  | Dynamic (15-30%)      | 62%      | 28%            | 10%                   |
  | Disruptive (>30%)     | 50%      | 34%            | 16%                   |

- **Trigger:** Quarterly CronJob evaluates velocity and adjusts team focus.

### Layer 3: Execution (Role-Stratified)

Governance responsibilities are distributed by organizational layer:

| Layer     | Horizon | Focus                          | Dashboard View             |
| --------- | ------- | ------------------------------ | -------------------------- |
| Executive | H3      | Market disruption, existential | 5-Year Strategic Radar     |
| Strategic | H2      | Capability building, new plays | 2-Year Opportunity Map     |
| Tactical  | H1      | Process optimization           | Quarterly Efficiency Board |
| Execution | H1      | Standardized task execution    | Sprint Dashboard           |

### Layer 4: Learning (Continuous Feedback Loop)

- **Pattern Detection:** AI agents identify successful "Discretionary Plays" (manual overrides that led to good outcomes).
- **Promotion Pipeline:**
  1.  Discretionary Play observed.
  2.  AI proposes new "Recommended Play" (draft policy change).
  3.  Human reviews and approves via PR to `policies/` repo.
  4.  Approved play becomes "Mandatory" (Standardization).
- **Governance Deltas:** Each policy change generates a `GovernanceDelta` event, linking the old policy, new policy, and the evidence that justified the change.

```
┌───────────────────────────────────────────────────────────────┐
│                    THE EVOLUTIONARY LOOP                      │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│   Discretionary Play (Human Action)                           │
│        │                                                      │
│        ▼                                                      │
│   AI Observes Success Pattern                                 │
│        │                                                      │
│        ▼                                                      │
│   AI Proposes Policy Update (PR to policies/)                 │
│        │                                                      │
│        ▼                                                      │
│   Human Approves (Merge)                                      │
│        │                                                      │
│        ▼                                                      │
│   Policy Becomes Mandatory (ADR-001)                          │
│        │                                                      │
│        ▼                                                      │
│   Freed Human Capacity → Allocated to H2/H3 (Fibonacci)       │
│        │                                                      │
│        └─────────────→ [Loop Continues] ◄─────────────────────┘
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## Consequences

### Positive

- **Self-Improvement:** The system gets smarter over time.
- **Strategic Agility:** Resources automatically shift based on market conditions.
- **Expertise Capture:** Human judgment is encoded into the playbook.
- **Auditability:** All evolution is traced via `GovernanceDelta` events.

### Negative

- **Complexity:** Requires multiple agent types and feedback mechanisms.
- **Trust Required:** Users must trust the AI's pattern detection.
- **Evolution Rate Tuning:** Balancing speed vs. stability is an ongoing calibration.

## Links

- [PRD-008: Prospection & Innovation Module](../requirements/PRD-008-prospection-module.md)
- [SDS-011: Sensing Layer](../specs/SDS-011-sensing-layer.md)
- [22 Paths Operational Manual](../../IAGPM_GenAI_Handbook/Reference.md)

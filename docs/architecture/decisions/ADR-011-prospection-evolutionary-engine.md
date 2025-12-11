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
  - **Market Velocity Agent:** Updates `Metric "MarketVelocity"`.
  - **Automation Rate Tracker:** Updates `Metric "AutomationRate"`.
  - **Wardley Map Updater:** Tracks component evolution via `ConceptChange`.
- **Output:** A materialized view of the `sea-dsl` graph state.

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

The **Evolutionary Mechanism**:

1.  **Guided Autonomy (Variant Generation):** Humans/AI use "Discretionary Plays" (Flows with `Permission`).
2.  **Constrained Execution (Selection):** Outcomes are measured against `Metric` targets.
3.  **Promotion:** Successful patterns are proposed as `ConceptChange` sets (e.g., turning a Discretionary Flow into a Mandatory Flow).
4.  **Feedback:** Freed capacity is reallocated via the Fibonacci ladder.

- **Governance Deltas:** Each evolution is represented as a `ConceptChange` linking old/new graph states.

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

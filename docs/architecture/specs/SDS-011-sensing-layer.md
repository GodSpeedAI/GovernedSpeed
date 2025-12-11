# SDS-011: Sensing Layer

**Version:** 1.0  
**Date:** 2025-12-09  
**Author:** Platform Team  
**Status:** Draft

---

## 1. Purpose

This document specifies the technical design for the **Sensing Layer** — the collection of agents and data pipelines that provide input to the Prospection & Evolutionary Engine (see [ADR-011](../decisions/ADR-011-prospection-evolutionary-engine.md)).

## 2. Scope

- **Market Velocity Agent:** Calculates the composite YoY market change metric.
- **Automation Rate Tracker:** Monitors the ratio of mandatory to discretionary tasks.
- **Wardley Map Updater:** (Future) AI agent for component evolution tracking.
- **Strategic Radar Output:** The `strategic_radar.json` data structure.

---

## 3. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SENSING LAYER                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐   │
│   │ Market Velocity │   │ Automation Rate │   │ Wardley Map     │   │
│   │ Agent           │   │ Tracker         │   │ Updater         │   │
│   └───────┬─────────┘   └───────┬─────────┘   └───────┬─────────┘   │
│           │                     │                     │             │
│           ▼                     ▼                     ▼             │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                   STRATEGIC RADAR AGGREGATOR                │   │
│   │                   (Generates strategic_radar.json)          │   │
│   └───────────────────────────────────────────────────────────────┘   │
│                                 │                                   │
│                                 ▼                                   │
│                   ┌─────────────────────────────┐                   │
│                   │ Allocation Engine (PRD-008) │                   │
│                   │ (Fibonacci Budget Calc)     │                   │
│                   └─────────────────────────────┘                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Components

### 4.1 Market Velocity Agent

**Purpose:** Calculate the composite YoY market change metric that determines the Fibonacci allocation gate.

**Inputs (Configuration):**

```yaml
# config/sensing/market_velocity.yaml
data_sources:
  - name: "internal_revenue"
    type: "database"
    query: "SELECT yoy_change FROM metrics WHERE metric_name = 'revenue' ORDER BY date DESC LIMIT 1"
    weight: 0.4
  - name: "new_entrant_rate"
    type: "api"
    endpoint: "https://market-data-provider.example.com/entrants?industry=ai"
    weight: 0.2
  - name: "tech_adoption"
    type: "manual" # Requires quarterly manual input
    weight: 0.2
  - name: "regulatory_change"
    type: "manual"
    weight: 0.2
```

**Output:**

```json
{
  "composite_yoy_change": 0.18,
  "gate": "DYNAMIC",
  "factors": {
    "internal_revenue": { "value": 0.12, "weight": 0.4 },
    "new_entrant_rate": { "value": 0.25, "weight": 0.2 },
    "tech_adoption": { "value": 0.2, "weight": 0.2 },
    "regulatory_change": { "value": 0.15, "weight": 0.2 }
  },
  "calculated_at": "2025-12-09T12:00:00Z"
}
```

**Gate Thresholds:**

| Composite YoY | Gate         |
| ------------- | ------------ |
| < 5%          | `STABLE`     |
| 5% - 14.9%    | `MODERATE`   |
| 15% - 29.9%   | `DYNAMIC`    |
| ≥ 30%         | `DISRUPTIVE` |

**Schedule:** Weekly (CronJob) for data collection; Gate determination is quarterly.

---

### 4.2 Automation Rate Tracker

**Purpose:** Monitor the degree to which H1 playbooks are automated, signaling freed capacity for H2/H3.

**Inputs:**

- Query the `governance_event` table for `event_type = 'policy_check_pass'` where `payload.task_type` indicates mandatory vs. discretionary.

**Calculation:**

```python
def calculate_automation_rate(events: list[dict]) -> float:
    mandatory_count = sum(1 for e in events if e.get('payload', {}).get('task_type') == 'mandatory')
    total_count = len(events)
    if total_count == 0:
        return 0.0
    return mandatory_count / total_count
```

**Output:**

```json
{
  "automation_rate": 0.72,
  "mandatory_task_count": 720,
  "discretionary_task_count": 280,
  "total_task_count": 1000,
  "period": "2025-Q4",
  "calculated_at": "2025-12-09T12:00:00Z"
}
```

**Thresholds for Action:**

| Rate   | Action                                                     |
| ------ | ---------------------------------------------------------- |
| < 60%  | No action. Focus on H1 optimization.                       |
| 60-74% | Allocate freed capacity to H2.                             |
| 75-89% | Allocate freed capacity to H3.                             |
| ≥ 90%  | Domain is "fully commoditized." Sunset H1, shift to H2/H3. |

**Schedule:** Weekly.

---

### 4.3 Wardley Map Updater (Future Phase)

**Purpose:** AI agent that ingests external signals (news, patents, research) and suggests updates to the organization's Wardley Map.

**Status:** TBD — Phase 4 implementation. See [PRD-008](../requirements/PRD-008-prospection-module.md) for requirements.

**Conceptual Flow:**

1.  Ingest news articles, patent filings, academic papers (via APIs or RAG).
2.  Identify mentions of known "components" from the active Wardley Map.
3.  Detect signal of evolution (e.g., "Component X now available as SaaS" → Genesis → Custom Build → Product → Commodity).
4.  Propose map update as a `governance_delta` (policy change suggestion).

---

## 5. Strategic Radar Aggregator

**Purpose:** Combine outputs from all sensing agents into a single `strategic_radar.json` for consumption by dashboards and the Allocation Engine.

**Output Schema:**

```json
{
  "timestamp": "2025-12-09T12:00:00Z",
  "market_velocity": {
    "composite_yoy_change": 0.18,
    "gate": "DYNAMIC",
    "factors": { ... }
  },
  "automation": {
    "rate": 0.72,
    "threshold_action": "allocate_h2"
  },
  "allocation_recommendation": {
    "h1": 0.62,
    "h2": 0.28,
    "h3": 0.10
  },
  "signals": [
    {
      "source": "news_feed",
      "headline": "Major competitor launches new AI product",
      "impact": "HIGH",
      "detected_at": "2025-12-08T09:00:00Z"
    }
  ]
}
```

**Storage:** Written to RES as an `artifact_index` record with `artifact_type: 'strategic_radar'`.

---

## 6. Data Flow Diagram

```
External Data Sources          Internal Data (RES)
        │                               │
        ▼                               ▼
┌───────────────────┐       ┌───────────────────────┐
│ Market Velocity   │       │ governance_event table│
│ Agent (API, DB)   │       │                       │
└───────┬───────────┘       └───────────┬───────────┘
        │                               │
        ▼                               ▼
┌───────────────────────────────────────────────────┐
│                   Strategic Radar                 │
│                   Aggregator                      │
└───────────────────────────────────────────────────┘
                        │
                        ▼
               strategic_radar.json
                        │
                        ▼
          ┌─────────────────────────────┐
          │ Allocation Engine / Dashboards│
          └─────────────────────────────┘
```

---

## 7. API Endpoints (Internal)

| Endpoint                            | Method | Description                                 |
| ----------------------------------- | ------ | ------------------------------------------- |
| `/internal/sensing/market-velocity` | GET    | Returns latest Market Velocity calculation. |
| `/internal/sensing/automation-rate` | GET    | Returns latest Automation Rate calculation. |
| `/internal/sensing/strategic-radar` | GET    | Returns latest aggregated Strategic Radar.  |
| `/internal/sensing/trigger-recalc`  | POST   | Manually trigger a recalculation.           |

---

## 8. Dependencies

- [ADR-011: Prospection & Evolutionary Engine](../decisions/ADR-011-prospection-evolutionary-engine.md)
- [PRD-008: Prospection & Innovation Module](../requirements/PRD-008-prospection-module.md)
- [SDS-001: Evidence Fabric Schemas](./SDS-001-evidence-fabric-schemas.md) (for querying `governance_event`)

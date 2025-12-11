# PRD-010: Governance Cockpit (UI)

**Version:** 1.0  
**Date:** 2025-12-10  
**Author:** Product Team  
**Status:** Draft

---

## 1. Overview

This document defines the requirements for the **Governance Cockpit** — the web-based user interface that serves as the "Command Center" for the Governed Speed platform. It replaces manual governance committees and spreadsheet tracking.

### 1.1 Problem Statement

The platform generates massive amounts of data (evidence, risk snapshots, case states). Without a unified UI, stakeholders cannot visualize risk, approve policy changes, or execute discretionary plays.

### 1.2 Goals

1.  **Visibility:** Single pane of glass for Risk, Speed, and Quality metrics.
2.  **Actionability:** Enable humans to execute **CMMN Discretionary Plays** directly from the UI.
3.  **Role-Based Views:** Tailored experiences for Executives (H3), Strategists (H2), and Operators (H1).

---

## 2. Target Users

| Persona             | Use Case                                                           |
| ------------------- | ------------------------------------------------------------------ |
| **Executive**       | "Show me the 5-year Strategic Radar and major H3 bets."            |
| **Governance Lead** | "Show me the current Risk Posture and pending Policy Deltas."      |
| **Developer**       | "Show me why my build failed and how to fix the policy violation." |
| **Case Worker**     | "Show me my active Cases and available Discretionary Plays."       |

---

## 3. Functional Requirements

### 3.1 Dashboard Layouts (Role-Stratified)

- **FR-1.1:** **Executive View (H3):** Strategic Radar, Market Velocity signals, Fibonacci Allocation variance.
- **FR-1.2:** **Operations View (H1):** CI/CD velocity, Blocking Policy count, Active Incidents.
- **FR-1.3:** **Compliance View:** Evidence coverage heatmaps, Audit readiness score.

### 3.2 Playbook Execution Interface

- **FR-2.1:** Users MUST be able to view details of an active CMMN Case (from PRD-009).
- **FR-2.2:** Users MUST be able to select and execute **Discretionary Tasks** for a case.
- **FR-2.3:** The UI MUST prompt for **Justification** when a discretionary task is chosen.

### 3.3 Policy Management

- **FR-3.1:** View active Policy-as-Code definitions (read-only render of `.sea` source).
- **FR-3.2:** View **Governance Deltas** (`ConceptChange` sets) and approve/reject them.
- **FR-3.3:** **System Graph Explorer:** Interactive node-link visualization of the live `sea-dsl` graph (Entities, Flows, Risks).

### 3.4 Risk & Evidence Explorer

- **FR-4.1:** Search/Filter `GovernanceEvent` history (fed by RES API).
- **FR-4.2:** Visual drill-down into `RiskSnapshots` by system or domain.

---

## 4. Non-Functional Requirements

- **NFR-1:** **Responsiveness:** < 2s load time for main dashboards.
- **NFR-2:** **Security:** OIDC Authentication with RBAC (ADR-008).
- **NFR-3:** **Tech Stack:** React/Next.js frontend, utilizing RES APis.

---

## 5. Success Metrics

| KPI                 | Target                                                            |
| ------------------- | ----------------------------------------------------------------- |
| _User Engagement_   | Daily Active Users (DAU) > 80% of governance team.                |
| _Decision Velocity_ | Mean time to approve Policy Delta < 48 hours.                     |
| _Playbook Usage_    | 100% of discretionary plays executed via Cockpit (vs email/chat). |

---

## 6. Dependencies

- [PRD-002: Risk & Evidence Service](./PRD-002-risk-evidence-service.md) (Data Source)
- [PRD-009: Playbook & CMMN Engine](./PRD-009-playbook-cmmn-engine.md) (Action Source)
- [ADR-008: Security Model](../decisions/ADR-008-security-zero-trust.md)

---

## 7. Open Questions

1.  Do we build a custom UI or use a low-code platform (e.g., Retool) for MVP?
    - _Recommendation: Custom Next.js app for long-term flexibility and "Premium" feel._

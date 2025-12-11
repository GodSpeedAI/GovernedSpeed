# PRD-009: Playbook & CMMN Execution Engine

**Version:** 1.0  
**Date:** 2025-12-10  
**Author:** Architecture Team, COE Logic  
**Status:** Draft

---

## 1. Overview

This document defines the requirements for the **Playbook & CMMN Execution Engine** — the operational core that translates strategic "Playbooks" into executable "Cases" managed by both humans and AI agents.

### 1.1 Problem Statement

Governance strategies (e.g., "handle high-risk data leak") are often documented in static PDFs or Wikis, making them hard to execute consistently or improve. We need a system that makes these strategies **executable**, **adaptive**, and **measurable**.

### 1.2 Goals

1.  **Standardization:** Enforce mandatory compliance steps for every case.
2.  **Adaptivity:** Empower humans to choose discretionary plays based on context.
3.  **Hybrid Execution:** Orchestrate hand-offs between AI agents (automation) and humans (judgment).
4.  **Learning:** Capture data on discretionary choices to feed the Evolutionary Engine.

---

## 2. Target Users

| Persona           | Needs                                                               |
| ----------------- | ------------------------------------------------------------------- |
| **Case Worker**   | "Tell me what I MUST do, and show me what I CAN do."                |
| **Process Owner** | Define and update Playbooks without code changes.                   |
| **AI Agent**      | Monitor cases for triggers; suggest plays; execute routine tasks.   |
| **Auditor**       | Trace who performed what action and why (especially discretionary). |

---

## 3. Functional Requirements

### 3.1 Playbook Definitions (Design Time)

- **FR-1.1:** The engine MUST load Playbooks defined in **SEA-DSL** (see SDS-012).
- **FR-1.2:** A Playbook MUST define:
  - **Situation:** Trigger condition.
  - **Mandatory Tasks:** Steps that autostart.
  - **Discretionary Plays:** Optional steps enabled by Sentries.
- **FR-1.3:** Changes to Playbooks MUST be version-controlled (GitOps).

### 3.2 CMMN Execution (Runtime)

- **FR-2.1:** The engine MUST instantiate a **Case** when a Situation triggers.
- **FR-2.2:** The Case MUST maintain a **Case File** (context data) accessible via API.
- **FR-2.3:** The engine MUST support **Sentries** (event-driven gates) to enable/disable tasks dynamically.
- **FR-2.4:** The engine MUST log every state transition (Active, Completed, Terminated).

### 3.3 AI Integration

- **FR-3.1:** The engine MUST expose a **Sentry Interface** for AI agents to trigger tasks based on external events (e.g., "Log analysis detects severity > 4").
- **FR-3.2:** The engine MUST expose an **Advisor Interface** to suggest Discretionary Plays to human users (e.g., "80% of similar cases used 'Engage Tier 3'").

### 3.4 Governance & Audit

- **FR-4.1:** All Discretionary Play executions MUST require a "Justification" (or link to context).
- **FR-4.2:** The engine MUST emit `GovernanceEvent` records for all task completions to RES.

---

## 4. Non-Functional Requirements

- **NFR-1:** Flexibility: Support ad-hoc tasks (runtime definition) for purely novel situations (H2/H3).
- **NFR-2:** Reliability: Case state must persist across restarts.
- **NFR-3:** Scalability: Support 10,000 active concurrent cases.

---

## 5. Success Metrics (KPIs)

| KPI                   | Target                                                         |
| --------------------- | -------------------------------------------------------------- |
| _Playbook Adherence_  | 100% of Mandatory tasks completed.                             |
| _Discretionary Usage_ | Track % of cases using discretionary plays (Evolution signal). |
| _Resolution Time_     | Reduce Mean Time to Resolve (MTTR) by 30% vs manual.           |

---

## 6. Dependencies

- [ADR-012: Playbook & CMMN Architecture](../decisions/ADR-012-playbook-cmmn-architecture.md)
- [SDS-012: Playbook Schema](../specs/SDS-012-playbook-schema.md)

---

## 7. Open Questions

1.  Should we use an off-the-shelf CMMN engine (Camunda) or build a lightweight runner?
    - _Decision: Start with lightweight custom runner for MVP, migrate to Camunda if complexity grows._

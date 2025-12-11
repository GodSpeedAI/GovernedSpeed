# ADR-012: Playbook & CMMN Architecture

**Status:** Accepted  
**Date:** 2025-12-10  
**Deciders:** Architecture Team, COE Logic  
**Technical Story:** Implement a formal "Playbook" layer to bridge high-level strategy and low-level execution, using CMMN (Case Management Model and Notation) for adaptive orchestration.

---

## Context and Problem Statement

Process automation (BPMN) is too rigid for the dynamic, knowledge-intensive nature of governed speed. Pure "human judgment" is unscalable and hard to govern. We need a middle ground that provides:

1.  **Standardization:** "Mandatory" tasks that must always happen (compliance).
2.  **Flexibility:** "Discretionary" tasks that humans/AI can choose based on context.
3.  **Traceability:** A record of _why_ a discretionary path was chosen.

## Decision Drivers

- **Adaptivity:** The system must handle "unknown unknowns" without breaking.
- **Institutional Memory:** Successful operational patterns (plays) must be captured and reused.
- **Hybrid Intelligence:** We need a unified runtime for Human + AI collaboration.

## Decision Outcome

We will adopt a **Playbook-CMMN Architecture**:

### 1. The Playbook Layer (Design Time)

- **Definition:** Playbooks are defined using **SEA-DSL** (Semantic Enterprise Architecture DSL).
- **Rationale:** SEA-DSL provides a strongly-typed, compilable foundation for defining logic (Sentries) and state (Case File) compared to loose JSON schemas.
- **Components:**
  - **Situation Context** (`Entity` / `Resource`): Defines the case file structure and involved business objects.
  - **Mandatory Procedures** (`Flow` + `Obligation`): Non-negotiable tasks enforced by policy obligations.
  - **Discretionary Plays** (`Flow` + `Permission`): Optional actions available to the case worker, enabled by permissions.
  - **Decision Rules** (`Policy`): Logic (Sentries) that governs the entry criteria and applicability of plays.

### 2. The CMMN Execution Layer (Runtime)

- **Engine:** A lightweight SEA-DSL runtime (Rust/WASM) acts as the CMMN-compatible engine.
- **Execution Flow:**
  - **Case Plan Model:** The parsed `.sea` Playbook file.
  - **Sentries:** Evaluated via `graph.evaluate_policy()` (Policy Engine).
  - **Case File:** The graph instance containing `Instances` of Entities/Resources.

### 3. AI Agent Integration

- **Sentry Agents:** AI agents monitor the "Case File" and trigger Sentries when conditions are met.
- **Advisor Agents:** Suggest Discretionary Plays to human workers based on historical success rates.

## Consequences

### Positive

- **Type Safety & Validation:** `sea-dsl` ensures that Sentries only reference existing data fields, preventing runtime errors.
- **Unified Logic:** The same `Policy` engine used for governance also drives playbook execution.
- **Evolutionary Data:** Discretionary choices are captured as graph mutations, perfectly suited for the Evolutionary Engine.

### Negative

- **Learning Curve:** Operators need to understand SEA-DSL concepts (though simpler GUIs can abstract this).
- **Engine Logic:** Requires building a bespoke (but lightweight) runtime loop around the SEA-DSL core.

## Links

- [ADR-011: Prospection & Evolutionary Engine](./ADR-011-prospection-evolutionary-engine.md)
- [PRD-009: Playbook & CMMN Execution Engine](../requirements/PRD-009-playbook-cmmn-engine.md)
- [SDS-012: Playbook Schema & CMMN Mapping](../specs/SDS-012-playbook-schema.md)

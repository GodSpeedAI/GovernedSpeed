# 🧭 Governed Speed × IAGPM Implementation Roadmap

## 1. Executive Summary

This roadmap outlines the strategic execution plan to evolve the current **Governed Speed** MVP into a fully realized **IAGPM-GenAI Platform**. The goal is to bridge the gap between the existing basic implementation and the comprehensive vision of "Executable Trust" — integrating Governance, Speed, and Learning into a unified operating system.

**Current State**: MVP with basic Policy-as-Code, Docker Compose/Helm scaffolding, and rudimentary CI.  
**Target State**: A self-governing AI delivery system with full auditability (ISO 42001/EU AI Act), runtime safety, and a sophisticated **Evolutionary Engine** that automates organizational learning and prospection.

---

## 2. Phase 1: Foundation & "The Leap" (Days 0–30)

**Focus**: Architectural Definition, Baseline Integrity, and Pilot Integration.

### 2.1 Architectural Documentation & Alignment

_Rationale: To enable "Governed Speed", we must first codify the laws and designs (ADRs/PRDs) that the system will enforce, including the new Prospection & Evolution layers._

- **[Doc] Instantiate Architecture Library**: Create `docs/architecture/` structure.
- **[Doc] Author Core ADRs** (Architecture Decision Records):
  - `ADR-001`: Governance as Code Pattern (Define YAML schema)
  - `ADR-002`: Evidence Fabric Architecture (libSQL → Postgres flow)
  - `ADR-003`: Embedded Governance in CI/CD (Pipeline gates)
  - `ADR-007`: Lightweight Embedded Evidence Journal (libSQL adoption)
  - `ADR-008`: Security Model & Zero-Trust Access
  - `ADR-011`: **Prospection & Evolutionary Engine** (Defining the H1/H2/H3 horizons & Fibonacci scaling logic).
- **[Doc] Draft Primary PRDs** (Product Requirements):
  - `PRD-001`: Governed Speed CI/CD Module
  - `PRD-002`: Risk & Evidence Service (RES) API
  - `PRD-008`: **Prospection & Innovation Module** (Wardley Mapping agents & Budgeting logic).
- **[Doc] Define System Specs (SDSs)**:
  - `SDS-001`: Evidence Fabric Schemas (Table definitions)
  - `SDS-002`: Policy Gate specs (Input/Output contracts)
  - `SDS-011`: **Sensing Layer** (Data collectors for Automation Rates & Market Velocity).

### 2.2 Core Component Implementation (The Integrated Spine)

- **[Code] Risk & Evidence Service (RES)**:
  - Flesh out `services/risk-evidence-service` from skeleton to basic CRUD.
  - Implement **SDS-001** Schema (Events, Risks, Artifacts).
  - Add SQLite (libSQL) local journaling capability.
- **[Code] Policy Gateway Enhancements**:
  - Implement **SDS-003** Sidecar pattern constraints.
  - Ensure "Fail-Closed" logic (`ADR-004`) is strictly enforced in `policy-gateway`.
- **[Ops] CI/CD Pipeline Adjustment**:
  - Update `.github/workflows/governed-speed-ci.yml` to strictly enforce `ADR-003` gates.

### 2.3 Operational "Leap" (Pilot)

- **[Ops] Pilot Deployment**: Deploy the stack to a dev cluster/namespace.
- **[Metrics] Baseline Capture**: Establish initial values for:
  - _Commit-to-Deploy Time_
  - _Evidence Coverage_ (Target: >50% for pilot)
  - _Automation Rate_ (Baseline for "Sensing" layer).

---

## 3. Phase 2: Maturity & "The Channel" (Days 30–60)

**Focus**: System Hardening, Security, and Production Readiness.

### 3.1 Advanced Architecture & Security

- **[Doc] Finalize Security Docs**:
  - `ADR-008`: Zero-Trust details.
  - `ADR-009`: Data Retention/Privacy.
  - `PRD-006`: Security & Privacy Controls.
- **[Code] Secret Management**:
  - Implement **Sealed Secrets** or **External Secrets Operator** (ESO) per `PROJECT_STATE.md` gaps.
  - Secure vLLM API keys and Database credentials.
- **[Code] Testing Suite (Critical Gap)**:
  - Implement Unit Tests (`tests/unit/`) for Gateway, RES, and **Sensing Agents** (Target: 80% coverage).
  - Implement Integration Tests (`tests/integration/`) for inter-service contracts.

### 3.2 vLLM & Runtime Control

- **[Code] Production vLLM Integration**:
  - Transition from "Mock" to real vLLM deployment (GPU enabled).
  - Implement Runtime Policy Gateway (Sidecar) for real-time prompt/response filtering.
  - Configure Model Storage (PVC vs Download-on-start) per **SDS-003**.

### 3.3 Dashboarding & Visibility

- **[Code] Governance Dashboards**:
  - Implement **PRD-003** (Grafana tiles).
  - Visualize "Governed Speed KPI One-Pager" metrics (Velocity, Integrity, Reliability).
  - **New View**: "Prospection Radar" — Visualizing H1/H2/H3 capacity allocation vs Targets.

---

## 4. Phase 3: The Evolutionary Engine & "The Reckoning" (Days 60–90)

**Focus**: Continuous Improvement, Prospection, and "Constrained Evolution".

### 4.1 The Evolutionary Engine (Core Logic)

- **[Code] Implement "Constrained Evolution" Logic**:
  - **Formula**: `Evolution = Guided Autonomy × Constrained Execution`.
  - **Mechanism**: Build the feedback loop where successful "Discretionary Plays" (manual overrides, new patterns) are detected by AI agents and proposed as "Standardized Policy" (H1).
- **[Code] Role-Stratified Dashboards**:
  - **Executive (H3)**: View 5yr horizons, market disruption signals (`SDS-011`).
  - **Strategic (H2)**: Competitor moves, capability gaps.
  - **Tactical (H1)**: Process optimization, automation candidates.

### 4.2 Prospection & Fibonacci Budgeting

- **[Code] Dynamic Resource Allocation**:
  - Implement the **Fibonacci Exploration Ladder** logic.
  - **Input**: Market Velocity (YoY change rate).
  - **Output**: Budget recommendation (e.g., Stable Market → 89% H1 / 8% H2 / 3% H3).
- **[Ops] Sensing Layer Activation**:
  - Deploy **Continuous Background Scanning** agents (Wardley Map updates).
  - Deploy **Threshold-Based Triggers** (e.g., "If Automation Rate > 90% → Shift resources to H2").

### 4.3 Policy Sandbox & Simulation

- **[Feature] Policy Sandbox**:
  - Allow "Dry Run" of new policies against historical traffic.
  - **Simulation**: Test new "Fibonacci Allocations" on past data to see if we would have caught disruption events.

---

## 5. Phase 4: Certification & "The Landing" (Day 90+)

**Focus**: External Audit, Certification (ISO/EU AI Act), and Scaling.

### 5.1 Certification Readiness

- **[Doc] Audit Exports**:
  - Implement **PRD-007** (Audit Export Pack).
  - Create automated `/v1/exports/audit` endpoint in RES.
- **[Doc] Evolutionary Traceability**:
  - Prove to auditors (ISO 42001) that the "Self-Learning" system has human-in-the-loop oversight for policy updates.

### 5.2 Scale & Optimization

- **[Ops] Tuning the Evolution Rate**:
  - Tune the speed of the "Standardization Cycle" based on domain risk (e.g., Slow for Legal, Fast for Content).

## 6. Detailed Prospection Architecture (Technical Specification)

### 6.1 Role-Stratified Temporal Horizons

- **Implementation**: RBAC-scoped views in the Governance Cockpit.
- **Data Flow**:
  - `Execution` (Logs) → `Tactical` (Optimization Signals).
  - `Tactical` (Capacity Reports) → `Strategic` (Reallocation Triggers).
  - `Strategic` (Pattern Detection) → `Executive` (Disruption Alerts).

### 6.2 The Fibonacci Budgeting Algorithm

- **Logic**:
  ```python
  def calculate_budget(yoy_velocity: float) -> dict:
      if yoy_velocity < 0.05: return {"H1": 0.89, "H2": 0.08, "H3": 0.03} # Stable
      if yoy_velocity < 0.15: return {"H1": 0.76, "H2": 0.18, "H3": 0.06} # Moderate
      if yoy_velocity < 0.30: return {"H1": 0.62, "H2": 0.28, "H3": 0.10} # Dynamic
      return {"H1": 0.50, "H2": 0.34, "H3": 0.16} # Disruptive
  ```
- **Trigger**: Quarterly CronJob or "Event-Driven" override.

### 6.3 Multi-Modal Trigger System

1.  **Always-On**: Vector search on news/patents (component evolution).
2.  **Threshold**: `Check_Automation_Rate` job (liberates capacity).
3.  **Event-Driven**: Manual "Panic Button" for C-Suite (immediate H3 shift).

---

## 7. Implementation Checklist (Immediate Next Steps)

1.  [ ] **Create Directory**: `mkdir -p docs/architecture/{decisions,requirements,specs}`
2.  [ ] **Draft ADR-001**: Define the YAML Policy-as-Code structure officially.
3.  [ ] **Draft ADR-011**: Define the Prospection & Evolutionary Engine.
4.  [ ] **Draft PRD-008**: Define the Sensing Agents & Dashboard widgets.
5.  [ ] **Repo Cleanup**: Organize existing `docs/Reference` content.

---

_Plan created based on "Governed Speed × IAGPM Framework" synthesis, "Prospection Architecture", and "Evolutionary Engine" logic._

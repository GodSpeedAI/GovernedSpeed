# Governed Speed Architecture Library

This directory contains the canonical architectural documentation for the **Governed Speed × IAGPM Platform**.

---

## 📂 Structure

```
docs/architecture/
├── README.md             # This file
├── decisions/            # Architecture Decision Records (ADRs)
├── requirements/         # Product Requirements Documents (PRDs)
└── specs/                # System Design Specifications (SDSs)
```

---

## 📜 Architecture Decision Records (ADRs)

ADRs document significant, often irreversible, design decisions. Each ADR captures the context, options considered, and rationale.

| ID                                                              | Title                                          | Status   |
| --------------------------------------------------------------- | ---------------------------------------------- | -------- |
| [ADR-001](decisions/ADR-001-governance-as-code.md)              | Governance as Code Pattern (SEA-DSL)           | Accepted |
| [ADR-002](decisions/ADR-002-evidence-fabric.md)                 | Evidence Fabric Architecture                   | Accepted |
| [ADR-003](decisions/ADR-003-embedded-governance-cicd.md)        | Embedded Governance in CI/CD                   | Accepted |
| [ADR-007](decisions/ADR-007-libsql-journal.md)                  | Lightweight Embedded Evidence Journal          | Accepted |
| [ADR-008](decisions/ADR-008-security-zero-trust.md)             | Security Model & Zero-Trust Access             | Accepted |
| [ADR-011](decisions/ADR-011-prospection-evolutionary-engine.md) | Prospection & Evolutionary Engine              | Accepted |
| [ADR-012](decisions/ADR-012-playbook-cmmn-architecture.md)      | Playbook & CMMN Architecture                   | Accepted |
| [ADR-013](decisions/ADR-013-handbook-as-code.md)                | Handbook as Code & Operational Source of Truth | Accepted |

---

## 📋 Product Requirements Documents (PRDs)

PRDs translate architecture into buildable product modules, defining functional and non-functional requirements.

| ID                                                       | Title                            | Status |
| -------------------------------------------------------- | -------------------------------- | ------ |
| [PRD-001](requirements/PRD-001-cicd-module.md)           | Governed Speed CI/CD Module      | Draft  |
| [PRD-002](requirements/PRD-002-risk-evidence-service.md) | Risk & Evidence Service (RES)    | Draft  |
| [PRD-008](requirements/PRD-008-prospection-module.md)    | Prospection & Innovation Module  | Draft  |
| [PRD-009](requirements/PRD-009-playbook-cmmn-engine.md)  | Playbook & CMMN Execution Engine | Draft  |
| [PRD-010](requirements/PRD-010-governance-cockpit.md)    | Governance Cockpit (UI)          | Draft  |

---

## 🧱 System Design Specifications (SDSs)

SDSs provide low-level technical designs, including database schemas, API contracts, and component specifications.

| ID                                                  | Title                          | Status |
| --------------------------------------------------- | ------------------------------ | ------ |
| [SDS-001](specs/SDS-001-evidence-fabric-schemas.md) | Evidence Fabric Schemas        | Draft  |
| [SDS-002](specs/SDS-002-policy-gate-specs.md)       | Policy Gate Specifications     | Draft  |
| [SDS-011](specs/SDS-011-sensing-layer.md)           | Sensing Layer                  | Draft  |
| [SDS-012](specs/SDS-012-playbook-schema.md)         | Playbook Schema & CMMN Mapping | Draft  |

---

## 🔗 Cross-Reference Map

```mermaid
graph LR
    subgraph "Decisions (ADRs)"
        A1[ADR-001: Gov-as-Code (SEA-DSL)]
        A2[ADR-002: Evidence Fabric]
        A3[ADR-003: CI/CD Gate]
        A7[ADR-007: libSQL]
        A8[ADR-008: Security]
        A11[ADR-011: Evolution]
        A12[ADR-012: Playbooks (CMMN)]
        A13[ADR-013: Handbook-as-Code]
    end

    subgraph "Requirements (PRDs)"
        P1[PRD-001: CI/CD Module]
        P2[PRD-002: RES API]
        P8[PRD-008: Prospection]
        P9[PRD-009: Playbook Engine]
        P10[PRD-010: Cockpit UI]
    end

    subgraph "Specs (SDSs)"
        S1[SDS-001: Schemas]
        S2[SDS-002: Policy Gate]
        S11[SDS-011: Sensing]
        S12[SDS-012: Playbook Schema]
    end

    A1 --> P1
    A1 --> S2
    A2 --> P2
    A2 --> S1
    A3 --> P1
    A7 --> S1
    A8 --> P2
    A11 --> P8
    A11 --> S11
    A12 --> P9
    A12 --> P10
    A12 --> S12
    A13 --> P10
    P1 --> S2
    P2 --> S1
    P8 --> S11
    P9 --> S12
    P10 --> P2
```

---

## ✅ How to Contribute

1.  **New ADR**: Copy an existing ADR template. Number sequentially.
2.  **New PRD**: Base on a linked ADR. Define user personas and functional requirements.
3.  **New SDS**: Link to the relevant PRD. Include schemas, API contracts, and data flows.
4.  **Review Process**: All architectural docs require PR review from at least one peer.

---

_This library is the single source of truth for how Governed Speed is designed and built._

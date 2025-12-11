# 📘 Handbook Refactoring Plan: From "Manual" to "Executable"

**Status:** Draft  
**Target Date:** Phase 1.2 (Immediate)  
**Dependencies:** `ADR-012`, `PRD-009`, `governed_speed_implementation_roadmap.md`

---

## 1. Objective

Refactor the existing `docs/IAGPM_GenAI_Handbook` to align with the **Governed Speed × IAGPM Platform** architecture. The core documentation will be generated from **SEA-DSL** strings, rendering the static handbook obsolete.

- **From:** A manual, checklist-driven guide for committees.
- **To:** An "Operational Manual" for an automated, self-learning system.

## 2. Core Strategy: "Documentation as Software"

The handbook will no longer be a static PDF-like repo. It will be the **User Guide** for the platform we are building.

| Old Handbook Concept     | New Platform Equivalent     | Refactoring Action                         |
| ------------------------ | --------------------------- | ------------------------------------------ |
| **Manual Checklists**    | **CI/CD Gates**             | Rewrite: "How to configure pipeline gates" |
| **Risk Register Xlsx**   | **RES Risk Snapshots**      | Rewrite: "Querying the Risk API"           |
| **Governance Committee** | **Governance Cockpit**      | Rewrite: "Using the Dashboard & Playbooks" |
| **Policy Templates**     | **SEA-DSL Policy Corpus**   | Link to `policies/*.sea`                   |
| **Intake Process**       | **CMMN Case Instantiation** | Explain "Playbook Triggers"                |

## 3. Directory Restructuring

We will move `docs/IAGPM_GenAI_Handbook` to `docs/handbook` and simplify.

```
docs/handbook/
├── 01_concept/           # The "Why" (Theory, Frameworks)
│   ├── framework_synthesis.md
│   └── evolutionary_engine.md
├── 02_platform/          # The "How" (User Guide)
│   ├── cicd_gates.md     # How to use PRD-001
│   ├── evidence_fabric.md# Understanding RES
│   └── policy_writing.md # How to write SEA-DSL Policies
├── 03_operations/        # The "Run" (Playbooks)
│   ├── playbook_design.md# Designing CMMN Playbooks
│   └── incident_response.md
└── 04_industry/          # Sector Specifics (Finance, Gov, etc.)
    └── ...
```

## 4. Work Items

### 4.1 Content Migration

1.  **Migrate Framework Theory**: Keep the strong theoretical synthesis (CPMAI, NIST, etc.) but frame it as the "Philosophy behind the Code".
2.  **Deprecate Templates**: Remove Word/Excel style templates. Replace with `sea-dsl` primitives (`Entity`, `Policy`, `Flow`).
3.  **Update "How-To"**:
    - Change "How to run a risk meeting" to "How to review a Risk Snapshot in the Cockpit".
    - Change "How to audit" to "How to generate an Evidence Export".

### 4.2 New Content Integration

1.  **Playbook Guide**: Add a section on designing Playbooks for the **PRD-009** Engine.
2.  **Evolutionary Guide**: Explain the **Fibonacci Hiring Model** and **Governance Delta** flow to managers.
3.  **Dashboard Guide**: Explain the **H1/H2/H3** role-stratified views.

### 4.3 Architecture Alignment

- **Create ADR-013 (Handbook as Code)**: Formalize this documentation strategy.
- **Create PRD-010 (Governance Cockpit)**: The UI that replaces the "Committee Meeting".

## 5. Implementation Steps

1.  **[Doc] Create Plan**: (This document).
2.  **[Decision] ADR-013**: Approve the refactoring strategy.
3.  **[Design] PRD-010**: Define the Cockpit UI requirements.
4.  **[Refactor] Move & Rename**: `git mv docs/IAGPM_GenAI_Handbook docs/handbook`.
5.  **[Refactor] Rewrite Content**: Iteratively update MD files to reference architectural components.
6.  **[Verify] Link Integrity**: Ensure all links to `docs/architecture` are valid.

---

## 6. Success Metrics

- **Consistency**: No instructions in the handbook contradict the code (e.g., "fill out this form" vs "run this script").
- **Completeness**: Every architectural component (RES, Gateway, Engine) has a User Guide section.
- **Clarity**: Users understand how "Manual Strategy" (Playbooks) drives "Automated Execution" (CMMN).

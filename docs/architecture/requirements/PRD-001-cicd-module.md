# PRD-001: Governed Speed CI/CD Module

**Version:** 1.0  
**Date:** 2025-12-09  
**Author:** Architecture Team  
**Status:** Draft

---

## 1. Overview

This document defines the product requirements for the **Governed Speed CI/CD Module** — the component responsible for embedding governance policy checks directly into the software delivery pipeline.

### 1.1 Problem Statement

Organizations shipping AI systems face a critical tension: governance slows down delivery, but lack of governance creates compliance and safety risks. The CI/CD Module resolves this by making governance a _built-in_ part of the pipeline, not a _bolt-on_ checkpoint.

### 1.2 Goals

1.  **Shift-Left Compliance:** Catch policy violations before code is merged.
2.  **Fail-Closed Enforcement:** Prevent non-compliant builds from deploying.
3.  **Evidence Generation:** Automatically produce audit artifacts for every build.
4.  **Developer Experience:** Provide fast, clear feedback in the Pull Request.

---

## 2. Target Users

| Persona          | Needs                                                                |
| ---------------- | -------------------------------------------------------------------- |
| **Developer**    | Fast feedback on policy violations; clear remediation guidance.      |
| **DevOps/MLOps** | Easy integration with existing CI/CD (GitHub Actions, GitLab CI).    |
| **Compliance**   | Verifiable proof that every build was checked against active policy. |
| **Auditor**      | Exportable evidence bundles linking builds to policy outcomes.       |

---

## 3. Functional Requirements

### 3.1 Policy Validation Gate

- **FR-1.1:** The module MUST load the active policy file (YAML) from the repository (`policies/` directory).
- **FR-1.2:** The module MUST validate build artifacts (e.g., evaluation reports, model cards) against policy thresholds.
- **FR-1.3:** The module MUST emit a clear `PASS` or `FAIL` status.
- **FR-1.4:** On `FAIL`, the module MUST block the pipeline (fail-closed behavior).
- **FR-1.5:** On `PASS`, the module MUST generate and upload an `evidence.json` artifact.

### 3.2 Reporting & Feedback

- **FR-2.1:** The module MUST output a human-readable summary to the CI log.
- **FR-2.2:** The module SHOULD post a comment to the Pull Request summarizing the check results.
- **FR-2.3:** The module MUST include specific remediation guidance for each failed threshold.

### 3.3 Integration Points

- **FR-3.1:** The module MUST be executable as a standalone CLI tool (`python tools/pac_ci.py`).
- **FR-3.2:** The module MUST be packageable as a GitHub Action for easy adoption.
- **FR-3.3:** The module SHOULD support GitLab CI and Azure DevOps as secondary platforms.

---

## 4. Non-Functional Requirements

- **NFR-1:** Latency: Policy check MUST complete in < 30 seconds for typical builds.
- **NFR-2:** Reliability: 99.9% success rate for the check step (excluding genuine policy failures).
- **NFR-3:** Security: Policy files MUST be validated against a JSON Schema to prevent injection.

---

## 5. Data Model (Evidence Output)

The `evidence.json` artifact produced by each successful run:

```json
{
  "build_id": "ci-12345",
  "timestamp": "2025-12-09T10:30:00Z",
  "policy_version": "adr-006-v1.2",
  "outcome": "PASS",
  "thresholds_checked": [
    {
      "name": "quality.pass_at_5",
      "target": 0.82,
      "actual": 0.85,
      "status": "PASS"
    },
    {
      "name": "fairness.subgroup_delta",
      "target_max": 0.05,
      "actual": 0.03,
      "status": "PASS"
    }
  ],
  "signature": "sha256:abcdef..."
}
```

---

## 6. Success Metrics (KPIs)

| KPI                      | Target                                                |
| ------------------------ | ----------------------------------------------------- |
| _Evidence Coverage_      | ≥ 95% of builds produce `evidence.json`.              |
| _Mean Check Latency_     | < 15 seconds (p95).                                   |
| _Developer Satisfaction_ | ≥ 80% positive feedback on clarity of error messages. |

---

## 7. Dependencies

- [ADR-001: Governance as Code](../decisions/ADR-001-governance-as-code.md)
- [ADR-003: Embedded Governance in CI/CD](../decisions/ADR-003-embedded-governance-cicd.md)
- [SDS-002: Policy Gate Specs](../specs/SDS-002-policy-gate-specs.md)

---

## 8. Open Questions

1.  Should the GitHub Action be published to the GitHub Marketplace?
2.  What is the process for requesting a policy override for a specific build?

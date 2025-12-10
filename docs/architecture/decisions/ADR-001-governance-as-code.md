# ADR-001: Governance as Code Pattern

**Status:** Accepted  
**Date:** 2025-12-09  
**Deciders:** Architecture Team, Governance Council  
**Technical Story:** Establish a foundational pattern for defining, versioning, and enforcing all governance rules as machine-readable code.

---

## Context and Problem Statement

The Governed Speed platform requires a consistent, auditable, and automatable method for managing governance policies across all AI systems. Manual policy management is slow, error-prone, and creates compliance gaps. We need a pattern that allows policies to be:

1.  Version-controlled alongside application code.
2.  Machine-validated at CI/CD time.
3.  Human-readable for audit purposes.

## Decision Drivers

- **Auditability:** ISO 42001 and EU AI Act require traceable policy enforcement.
- **Velocity:** Policies must not slow down deployment cycles.
- **Consistency:** Rules must be applied uniformly across all environments.
- **Extensibility:** New policy types must be easy to add.

## Considered Options

1.  **Option A: YAML-based Policy-as-Code (Selected)**

    - Policies defined in structured YAML files within the repository.
    - Validated by JSON Schema.
    - Parsed and enforced by the Policy Gateway and CI/CD pipelines.

2.  **Option B: Open Policy Agent (OPA) / Rego**

    - Powerful, but steep learning curve.
    - Overkill for current requirements.

3.  **Option C: Database-Driven Policies**
    - Policies stored in a central database.
    - Loses Git history and review benefits.

## Decision Outcome

**Chosen Option: Option A — YAML-based Policy-as-Code.**

All governance policies will be defined in YAML format within the `policies/` directory. Each policy file adheres to a strict JSON Schema (`specs/policy-schema.json`). The Policy Gateway and `pac_ci.py` tooling will parse and enforce these policies.

## Consequences

### Positive

- **Traceability:** Every policy change is a Git commit, providing full audit history.
- **Review Process:** Policies go through Pull Request review like code.
- **Automation:** Policies are automatically validated and deployed.
- **Accessibility:** YAML is human-readable for non-engineers (compliance officers, auditors).

### Negative

- **Schema Rigidity:** Changes to the policy schema require careful migration.
- **Tooling Dependency:** Requires custom tooling (`pac_ci.py`, Policy Gateway) to parse and enforce.

## Links

- [ADR-003: Embedded Governance in CI/CD](./ADR-003-embedded-governance-cicd.md)
- [SDS-002: Policy Gate Specs](../specs/SDS-002-policy-gate-specs.md)
- [policies/adr-006.embedded-governance.yaml](../../policies/adr-006.embedded-governance.yaml)

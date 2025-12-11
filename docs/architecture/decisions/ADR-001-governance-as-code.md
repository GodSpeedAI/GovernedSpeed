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

1.  **Option A: SEA-DSL Policies (Selected)**

    - Policies defined as `Policy` primitives in `*.sea` files.
    - Strongly typed against the Domain Model (Entities/Resources).
    - Compiled to Rust/WASM for high-performance enforcement in the Gateway.
    - Unifies Governance Logic with Playbook Logic (ADR-012).

2.  **Option B: YAML-based Policy-as-Code**

    - Flexible but structurally weak (string-based logic).
    - Disconnected from the Domain Model.

3.  **Option C: Open Policy Agent (OPA) / Rego**
    - Industry standard but introduces a separate language (Rego) disjoint from our Domain Graph.

## Decision Outcome

**Chosen Option: Option A — SEA-DSL Policies.**

All governance policies will be defined in `.sea` modules. The `sea-runtime` (Rust) will enforce these policies at the Gateway and CI/CD layers. This ensures that a policy like "No PII in Logs" is checked against the _actual_ definition of `Log` and `PII` in our system model.

## Consequences

### Positive

- **Type Safety:** Policies cannot reference non-existent fields or entities.
- **Unified Engine:** One runtime for Security, Compliance, and Playbooks.
- **Performance:** Pre-compiled WASM policy evaluation is faster than interpreting YAML/JSON.

### Negative

- **Bootstrapping:** Requires defining the Domain Model (Entities/Resources) before writing Policies.
- **Learning Curve:** Developers must learn SEA-DSL syntax (vs generic YAML).

## Links

- [ADR-003: Embedded Governance in CI/CD](./ADR-003-embedded-governance-cicd.md)
- [SDS-002: Policy Gate Specs](../specs/SDS-002-policy-gate-specs.md)
- [policies/adr-006.embedded-governance.yaml](../../policies/adr-006.embedded-governance.yaml)

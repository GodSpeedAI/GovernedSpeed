# ADR-003: Embedded Governance in CI/CD

**Status:** Accepted  
**Date:** 2025-12-09  
**Deciders:** Architecture Team, DevOps Team  
**Technical Story:** Integrate governance policy checks directly into the CI/CD pipeline to enforce compliance before deployment.

---

## Context and Problem Statement

Governance policies are ineffective if applied only at runtime. Violations discovered in production are costly to remediate. We need a "Shift-Left" approach where policies are validated at the earliest possible moment — during the CI/CD build.

## Decision Drivers

- **Speed:** Catch violations before they reach production.
- **Enforcement:** Make compliance non-negotiable (fail-closed).
- **Transparency:** Provide clear feedback to developers in the PR.
- **Auditability:** Record CI check results as governance evidence.

## Considered Options

1.  **Option A: Custom Python Gate (`pac_ci.py`) (Selected)**

    - A Python script that parses policy YAML, validates artifacts, and emits pass/fail.
    - Integrated as a GitHub Actions step.

2.  **Option B: Conftest / OPA in CI**

    - Uses Rego for policy evaluation.
    - More powerful, but requires Rego expertise.

3.  **Option C: No CI Gate (Runtime Only)**
    - Policies enforced only by the runtime Policy Gateway.
    - Risk: Violations reach production.

## Decision Outcome

**Chosen Option: Option A — Custom Python Gate (`pac_ci.py`).**

The `tools/pac_ci.py` script will be executed as a required step in the GitHub Actions workflow. It will:

1.  Load the active policy file (e.g., `policies/adr-006.embedded-governance.yaml`).
2.  Validate build artifacts (e.g., evaluation reports) against policy thresholds.
3.  Emit a `PASS` or `FAIL` status.
4.  On `FAIL`, the pipeline is blocked (Fail-Closed).

```yaml
# .github/workflows/governed-speed-ci.yml
jobs:
  governance-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Governance Gate
        run: python tools/pac_ci.py --config policies/adr-006.embedded-governance.yaml
```

## Consequences

### Positive

- **Shift-Left Compliance:** Violations caught before merge.
- **Developer Feedback:** Clear error messages in the PR.
- **Evidence Generation:** CI run logs become part of the audit trail.

### Negative

- **Maintenance:** Custom script requires ongoing upkeep.
- **Flexibility:** Less powerful than a full policy engine (OPA).

## Links

- [ADR-001: Governance as Code Pattern](./ADR-001-governance-as-code.md)
- [PRD-001: Governed Speed CI/CD Module](../requirements/PRD-001-cicd-module.md)
- [tools/pac_ci.py](../../../tools/pac_ci.py)

# SDS-002: Policy Gate Specifications

**Version:** 1.0  
**Date:** 2025-12-09  
**Author:** Platform Team  
**Status:** Draft

---

## 1. Purpose

This document specifies the input/output contracts, evaluation logic, and behavioral guarantees for the **Policy Gate** — the component that enforces governance policies in CI/CD pipelines (`pac_ci.py`) and at runtime (Policy Gateway sidecar).

## 2. Scope

- **CI/CD Gate (`pac_ci.py`):** Validates build artifacts against policy before merge/deploy.
- **Runtime Gate (Policy Gateway):** Filters prompts and outputs in real-time.

---

## 3. Policy File Schema

All policies are defined in YAML and validated against a JSON Schema.

**Policy File Structure:**

```yaml
# policies/my-policy.yaml
meta:
  policy_id: "my-policy-v1"
  version: "1.0.0"
  description: "Example governance policy"
  effective_date: "2025-01-01"

thresholds:
  quality:
    pass_at_5:
      target: 0.82
      operator: ">="
  fairness:
    subgroup_delta:
      target_max: 0.05
      operator: "<="
  safety:
    harmful_rate:
      target_max: 0.005
      operator: "<="

rules:
  - id: pii_block
    description: "Block prompts containing PII without lawful basis"
    when: "contains_pii == true AND lawful_basis == false"
    action: block
    message: "PII detected without lawful basis. Request blocked."

  - id: jailbreak_safe_mode
    description: "Redirect jailbreak attempts to safe mode"
    when: "jailbreak_score > 0.8"
    action: safe_mode
    message: "Potential jailbreak detected. Redirecting to safe response."
```

---

## 4. CI/CD Gate (`pac_ci.py`)

### 4.1 Input Contract

The script expects:

1.  `--config <path>`: Path to the YAML policy file.
2.  `--artifacts <path>`: Path to a JSON file containing evaluation results.

**Example `artifacts.json`:**

```json
{
  "quality": { "pass_at_5": 0.85 },
  "fairness": { "subgroup_delta": 0.03 },
  "safety": { "harmful_rate": 0.002 }
}
```

### 4.2 Evaluation Logic

For each threshold defined in the policy:

1.  Extract the actual value from `artifacts.json`.
2.  Compare against the target using the specified operator.
3.  Record `PASS` or `FAIL` for each threshold.
4.  Overall result is `PASS` only if ALL thresholds pass.

**Pseudocode:**

```python
def evaluate(policy, artifacts):
    results = []
    for category, metrics in policy['thresholds'].items():
        for metric_name, spec in metrics.items():
            actual = artifacts.get(category, {}).get(metric_name)
            if actual is None:
                results.append({'metric': metric_name, 'status': 'MISSING'})
                continue
            passed = compare(actual, spec['target'], spec.get('operator', '>='))
            results.append({'metric': metric_name, 'actual': actual, 'target': spec['target'], 'status': 'PASS' if passed else 'FAIL'})
    overall = 'PASS' if all(r['status'] == 'PASS' for r in results) else 'FAIL'
    return overall, results
```

### 4.3 Output Contract

**Exit Codes:**

- `0`: All thresholds passed.
- `1`: One or more thresholds failed.
- `2`: Configuration or input error.

**Stdout Output:**

```
=== Governed Speed Policy Gate ===
Policy: my-policy-v1
Artifacts: ./artifacts.json

[PASS] quality.pass_at_5: 0.85 >= 0.82
[PASS] fairness.subgroup_delta: 0.03 <= 0.05
[PASS] safety.harmful_rate: 0.002 <= 0.005

Overall: PASS
```

**Evidence Artifact (`evidence.json`):** (See PRD-001 for format)

---

## 5. Runtime Gate (Policy Gateway)

### 5.1 Endpoints

- `POST /filter/prompt`: Evaluate a prompt before sending to vLLM.
- `POST /filter/output`: Evaluate an LLM output before returning to user.

### 5.2 `/filter/prompt` Contract

**Request:**

```json
{
  "prompt": "string",
  "context": {
    "contains_pii": true,
    "lawful_basis": false,
    "jailbreak_score": 0.2,
    "user_id": "user-123",
    "session_id": "sess-abc"
  }
}
```

**Response:**

```json
{
  "allowed": false,
  "action": "block",
  "reasons": ["PII detected without lawful basis. Request blocked."],
  "request_id": "req-xyz"
}
```

### 5.3 `/filter/output` Contract

**Request:**

```json
{
  "output": "string (LLM response)",
  "context": {
    "request_id": "req-xyz",
    "harmful_content_score": 0.01
  }
}
```

**Response:**

```json
{
  "allowed": true,
  "action": "pass",
  "reasons": [],
  "request_id": "req-xyz"
}
```

### 5.4 Fail-Closed Behavior

If the Policy Gateway cannot evaluate a request (e.g., policy file missing, internal error), it MUST:

1.  Return `allowed: false` with `action: "error_block"`.
2.  Log the error as a `governance_event` with `event_type: 'policy_check_fail'`.

---

## 6. Rule Evaluation Engine

### 6.1 `when` Expression Syntax

The `when` clause uses a simple expression language:

- **Variables:** Any key from the `context` object (e.g., `contains_pii`, `jailbreak_score`).
- **Operators:** `==`, `!=`, `>`, `<`, `>=`, `<=`.
- **Logical:** `AND`, `OR`, `NOT` (uppercase).
- **Parentheses:** For grouping.

**Example:**

```yaml
when: "(contains_pii == true AND lawful_basis == false) OR jailbreak_score > 0.9"
```

### 6.2 Actions

| Action      | Description                               |
| ----------- | ----------------------------------------- |
| `pass`      | Allow the request to proceed.             |
| `block`     | Reject the request.                       |
| `safe_mode` | Redirect to a predefined safe response.   |
| `redact`    | Mask sensitive content before proceeding. |
| `log_only`  | Allow but flag for review.                |

---

## 7. Dependencies

- [ADR-001: Governance as Code](../decisions/ADR-001-governance-as-code.md)
- [ADR-003: Embedded Governance in CI/CD](../decisions/ADR-003-embedded-governance-cicd.md)
- [PRD-001: CI/CD Module](../requirements/PRD-001-cicd-module.md)
- [specs/openapi-policy-gateway.yaml](../../../specs/openapi-policy-gateway.yaml)

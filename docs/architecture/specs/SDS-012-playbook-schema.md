# SDS-012: Playbook Schema & CMMN Mapping

**Version:** 1.0  
**Date:** 2025-12-10  
**Author:** Architecture Team  
**Status:** Draft

---

## 1. Purpose

This document specifies the technical schema for **Playbooks** (design-time strategy) and their mapping to **CMMN Case Models** (runtime execution).

## 2. Scope

- **Playbook Schema:** JSON/YAML format for defining strategies.
- **CMMN 1.1 Mapping:** How Playbook elements translate to standard CMMN concepts.

---

## 3. Playbook Schema (SEA-DSL)

Playbooks are defined as **SEA-DSL** modules. The following example demonstrates the "Customer Churn Risk" playbook using the official DSL primitives.

```sea
@namespace "playbook.churn_risk"
@version "1.0.0"
@owner "Customer Success Ops"

// --- 1. THE CASE FILE DEFINITIONS (Context) ---
// The "Situation" is defined by the Entities and Resources involved
Entity "Customer" in commercial
Resource "ChurnScore" units
Resource "Discount"
Resource "ContractRenewal"

// --- 2. ROLES (The Team) ---
Role "AccountManager"
Role "NotifierAgent" // AI Agent

// --- 3. PLAYS (Tasks as Flows/Relations) ---

// Play A: Notify Executive (Mandatory)
// Modeled as a Flow of information
// Logic: If ChurnScore < 40, Agent MUST notify
Flow "ChurnAlert" from "NotifierAgent" to "AccountManager"

// Play B: Offer Discount (Discretionary)
// Modeled as providing a Resource to the Customer
// Logic: Can only offer if ChurnScore < 50
Flow "Discount" from "AccountManager" to "Customer"

// --- 4. SENTRIES (Logic) ---

// Sentry 1: Mandatory Trigger (Activation Condition)
// Modeled as an OBLIGATION: If condition met, Flow MUST exist
Policy entry_sentry_notify per Obligation priority 10 as:
    forall i in instances of "Customer":
        (i.churn_score < 40) implies (exists f in flows: f.resource = "ChurnAlert")

// Sentry 2: Applicability Rule (Enablement Condition)
// Modeled as a PERMISSION: Action is allowed only if condition met
Policy eligibility_sentry_discount per Permission as:
    forall i in instances of "Customer":
        (i.churn_score < 50)
```

---

## 4. CMMN Mapping Definition

| Playbook Concept    | CMMN 1.1 Element  | SEA-DSL Implementation                                     |
| ------------------- | ----------------- | ---------------------------------------------------------- |
| **Situation**       | `CasePlanModel`   | The `.sea` file module (namespace scope).                  |
| **Case File**       | `CaseFileItem`    | `Entity`, `Resource` definitions + runtime `Instance`.     |
| **Task / Play**     | `PlanItem`        | `Flow` (Action) or `Relation` (State Change).              |
| **Sentry (Entry)**  | `Sentry` (IfPart) | `Policy` type `Obligation`: Triggers mandatory actions.    |
| **Sentry (Enable)** | `Sentry` (IfPart) | `Policy` type `Permission`: Enables discretionary actions. |
| **Role**            | `Role`            | `Role` primitive.                                          |

---

## 5. Execution Lifecycle (Runtime)

1.  **Instantiation:**

    - Engine loads the `.sea` Playbook file (Design).
    - Engine triggers creates a `Graph` with `Instance` data (Runtime context e.g., `churn_score: 35`).

2.  **Sentry Evaluation:**

    - Engine calls `graph.evaluate_policy(entry_sentry_notify)`.
    - If Result = `False` (Obligation broken) -> **Trigger Mandatory Task**.
    - Engine calls `graph.evaluate_policy(eligibility_sentry_discount)`.
    - If Result = `True` (Permission granted) -> **Enable Discretionary UI Button**.

3.  **Action:**
    - User/Agent executes task.
    - Engine adds the resulting `Flow` or `Relation` to the Graph.
    - re-evaluate policies (Obligation now `True` -> Task Complete).

---

## 6. Dependencies

- [ADR-012: Playbook & CMMN Architecture](../decisions/ADR-012-playbook-cmmn-architecture.md)
- [PRD-009: Playbook Engine](../requirements/PRD-009-playbook-cmmn-engine.md)

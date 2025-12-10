# SDS-001: Evidence Fabric Schemas

**Version:** 1.0  
**Date:** 2025-12-09  
**Author:** Platform Team  
**Status:** Draft

---

## 1. Purpose

This document specifies the database schemas for the **Evidence Fabric** — the data layer that underlies the Risk & Evidence Service (RES) and local libSQL journals.

## 2. Scope

- **Central Store (PostgreSQL):** Schema for the RES production database.
- **Local Journal (libSQL):** Lightweight schema for edge buffering.

---

## 3. Core Entities

### 3.1 `governance_event`

The primary event log. All policy checks, validations, and governance decisions are recorded here.

**PostgreSQL Schema:**

```sql
CREATE TABLE governance_event (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    event_type TEXT NOT NULL CHECK (event_type IN (
        'policy_check_pass', 'policy_check_fail', 'override_granted',
        'risk_assessment', 'incident_opened', 'incident_resolved',
        'governance_delta', 'audit_export'
    )),
    system_id TEXT NOT NULL,          -- Identifier of the AI system being governed
    policy_id TEXT,                    -- Reference to the policy rule (e.g., 'adr-006.pii_block')
    build_id TEXT,                     -- CI build identifier (if applicable)
    payload JSONB NOT NULL,            -- Full event details
    hash TEXT NOT NULL,                -- SHA-256 of payload for tamper detection
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ge_timestamp ON governance_event(timestamp);
CREATE INDEX idx_ge_system_id ON governance_event(system_id);
CREATE INDEX idx_ge_event_type ON governance_event(event_type);
```

**libSQL Schema (Local Journal):**

```sql
CREATE TABLE governance_event (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    timestamp TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    event_type TEXT NOT NULL,
    system_id TEXT NOT NULL,
    policy_id TEXT,
    build_id TEXT,
    payload TEXT NOT NULL,             -- JSON string
    hash TEXT NOT NULL,
    shipped INTEGER DEFAULT 0          -- 0=pending, 1=shipped to RES
);
CREATE INDEX idx_shipped ON governance_event(shipped);
```

---

### 3.2 `risk_snapshot`

Point-in-time assessments of a system's overall risk posture.

**PostgreSQL Schema:**

```sql
CREATE TABLE risk_snapshot (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    system_id TEXT NOT NULL,
    risk_score REAL NOT NULL CHECK (risk_score >= 0 AND risk_score <= 1),
    risk_level TEXT NOT NULL CHECK (risk_level IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    contributing_factors JSONB NOT NULL,  -- Array of factor objects
    assessed_by TEXT NOT NULL,            -- 'automated' or user ID
    hash TEXT NOT NULL
);

CREATE INDEX idx_rs_system_id ON risk_snapshot(system_id);
CREATE INDEX idx_rs_timestamp ON risk_snapshot(timestamp);
```

**Example `contributing_factors`:**

```json
[
  {
    "factor": "fairness_subgroup_delta",
    "value": 0.04,
    "threshold": 0.05,
    "status": "ok"
  },
  {
    "factor": "harmful_output_rate",
    "value": 0.008,
    "threshold": 0.005,
    "status": "breach"
  }
]
```

---

### 3.3 `incident`

Tracks governance incidents from detection to resolution.

**PostgreSQL Schema:**

```sql
CREATE TABLE incident (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    system_id TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('SEV1', 'SEV2', 'SEV3', 'SEV4')),
    status TEXT NOT NULL CHECK (status IN ('OPEN', 'INVESTIGATING', 'MITIGATED', 'RESOLVED')),
    title TEXT NOT NULL,
    description TEXT,
    related_event_ids UUID[],             -- Links to governance_event records
    root_cause TEXT,
    remediation_notes TEXT,
    resolved_at TIMESTAMPTZ,
    resolved_by TEXT
);

CREATE INDEX idx_inc_status ON incident(status);
CREATE INDEX idx_inc_severity ON incident(severity);
```

---

### 3.4 `artifact_index`

Tracks all governance-related artifacts (model cards, evaluation reports, audit bundles).

**PostgreSQL Schema:**

```sql
CREATE TABLE artifact_index (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    artifact_type TEXT NOT NULL CHECK (artifact_type IN (
        'model_card', 'evaluation_report', 'audit_bundle', 'policy_snapshot'
    )),
    system_id TEXT NOT NULL,
    version TEXT NOT NULL,
    storage_uri TEXT NOT NULL,          -- e.g., s3://bucket/path, file://local/path
    hash TEXT NOT NULL,                 -- SHA-256 of the artifact file
    metadata JSONB
);

CREATE INDEX idx_ai_system_id ON artifact_index(system_id);
CREATE INDEX idx_ai_artifact_type ON artifact_index(artifact_type);
```

---

### 3.5 `governance_delta`

Tracks changes to the policy corpus (the "evolution" record).

**PostgreSQL Schema:**

```sql
CREATE TABLE governance_delta (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    change_type TEXT NOT NULL CHECK (change_type IN ('NEW_RULE', 'UPDATED_THRESHOLD', 'DEPRECATED_RULE')),
    before_policy_id TEXT,              -- NULL if new rule
    after_policy_id TEXT NOT NULL,
    justification_event_ids UUID[],     -- Links to governance_event records that justified the change
    pr_url TEXT,                        -- Link to the Pull Request
    approved_by TEXT NOT NULL
);

CREATE INDEX idx_gd_timestamp ON governance_delta(timestamp);
```

---

## 4. Tamper-Proofing

All tables with a `hash` column use SHA-256 to ensure data integrity.

**Hash Calculation (Python Example):**

```python
import hashlib
import json

def calculate_hash(payload: dict) -> str:
    """Calculate SHA-256 hash of a JSON payload."""
    canonical = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical.encode('utf-8')).hexdigest()
```

**Verification:** Periodically run a job to verify `hash` matches `payload` for all records.

---

## 5. Retention Policy

| Entity             | Retention Period | Rationale                       |
| ------------------ | ---------------- | ------------------------------- |
| `governance_event` | 7 years          | EU AI Act minimum               |
| `risk_snapshot`    | 7 years          | Align with events               |
| `incident`         | 10 years         | Longer for legal/forensic needs |
| `artifact_index`   | 7 years          | Align with events               |
| `governance_delta` | Indefinite       | Policy history is always needed |

---

## 6. Dependencies

- [ADR-002: Evidence Fabric Architecture](../decisions/ADR-002-evidence-fabric.md)
- [ADR-007: libSQL Journal](../decisions/ADR-007-libsql-journal.md)
- [PRD-002: Risk & Evidence Service](../requirements/PRD-002-risk-evidence-service.md)

# PRD-002: Risk & Evidence Service (RES)

**Version:** 1.0  
**Date:** 2025-12-09  
**Author:** Architecture Team  
**Status:** Draft

---

## 1. Overview

This document defines the product requirements for the **Risk & Evidence Service (RES)** — the central API and storage layer for all governance data in the Governed Speed platform.

### 1.1 Problem Statement

Governance data (policy checks, risk snapshots, incidents) is generated across multiple systems. Without a central, queryable store, generating audit reports is manual, time-consuming, and error-prone. RES provides a single source of truth for all governance evidence.

### 1.2 Goals

1.  **Centralization:** Aggregate evidence from all sources (CI/CD, Runtime Gateway, Manual Input).
2.  **Queryability:** Enable real-time dashboards and trend analysis.
3.  **Auditability:** Support tamper-proof exports for compliance audits.
4.  **Extensibility:** Easy to add new evidence types as the platform evolves.

---

## 2. Target Users

| Persona                | Needs                                                             |
| ---------------------- | ----------------------------------------------------------------- |
| **PMO / Governance**   | Dashboard views of risk posture, build evidence, incident trends. |
| **Compliance Officer** | Query evidence by date range, system, or policy.                  |
| **Auditor**            | Export signed evidence bundles (ISO 42001, EU AI Act format).     |
| **Developer/Ops**      | API access to log evidence and query for debugging.               |
| **AI Agent (Shipper)** | Bulk push evidence from local journals.                           |

---

## 3. Functional Requirements

### 3.1 Evidence API (CRUD)

- **FR-1.1:** The service MUST expose a REST API (`/v1/evidence`) for creating and querying `GovernanceEvent` records.
- **FR-1.2:** The service MUST support filtering by `event_type`, `timestamp`, `system_id`, and `policy_id`.
- **FR-1.3:** The service MUST support pagination for large result sets.
- **FR-1.4:** All records are **append-only**; the API MUST NOT support `DELETE` or `UPDATE` on evidence.

### 3.2 Risk Snapshot API

- **FR-2.1:** The service MUST expose `/v1/risk/snapshot` to create and query point-in-time risk assessments.
- **FR-2.2:** Snapshots MUST include: `system_id`, `timestamp`, `risk_score`, `contributing_factors` (JSON).

### 3.3 Incident API

- **FR-3.1:** The service MUST expose `/v1/incident` to create, query, and update incidents.
- **FR-3.2:** Incidents MUST have a lifecycle (`OPEN` → `INVESTIGATING` → `RESOLVED`).
- **FR-3.3:** The service MUST support linking incidents to `GovernanceEvent` records.

### 3.4 Audit Export API

- **FR-4.1:** The service MUST expose `/v1/exports/audit` to generate signed evidence bundles.
- **FR-4.2:** The bundle MUST include a manifest with SHA-256 hashes of all included files.
- **FR-4.3:** The bundle MUST be downloadable as a `.zip` or `.tar.gz` archive.
- **FR-4.4:** Bundles MUST be generatable with filters for specific frameworks (e.g., `?framework=iso42001`).

### 3.5 Webhooks

- **FR-5.1:** The service SHOULD support outgoing webhooks for key events:
  - `policy_fail`: Triggered when a governance check fails.
  - `incident_opened`: Triggered when a new incident is created.
  - `risk_threshold_exceeded`: Triggered when a risk snapshot crosses a defined threshold.

---

## 4. Non-Functional Requirements

- **NFR-1:** Availability: 99.5% uptime (SLO).
- **NFR-2:** Latency: API response time < 300ms (p95).
- **NFR-3:** Scalability: Handle 10,000 events/minute.
- **NFR-4:** Durability: No data loss. Backed by PostgreSQL with daily backups.
- **NFR-5:** Security: All endpoints secured via OAuth2/JWT. See [ADR-008](../decisions/ADR-008-security-zero-trust.md).

---

## 5. Data Model (Core Entities)

```sql
-- Central Postgres Schema (See SDS-001)
CREATE TABLE governance_event (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    event_type TEXT NOT NULL,
    system_id TEXT NOT NULL,
    policy_id TEXT,
    payload JSONB NOT NULL,
    hash TEXT NOT NULL -- SHA-256 of payload for tamper-proofing
);

CREATE TABLE risk_snapshot ( ... );
CREATE TABLE incident ( ... );
CREATE TABLE artifact_index ( ... );
```

---

## 6. Success Metrics (KPIs)

| KPI                    | Target                                            |
| ---------------------- | ------------------------------------------------- |
| _Audit Export Latency_ | < 60 seconds to generate a full audit bundle.     |
| _Traceable Decisions_  | 100% of governance events have a verifiable hash. |
| _API Uptime_           | ≥ 99.5% monthly.                                  |

---

## 7. Dependencies

- [ADR-002: Evidence Fabric Architecture](../decisions/ADR-002-evidence-fabric.md)
- [ADR-007: libSQL Journal](../decisions/ADR-007-libsql-journal.md)
- [SDS-001: Evidence Fabric Schemas](../specs/SDS-001-evidence-fabric-schemas.md)
- [specs/openapi-risk-evidence-service.yaml](../../../specs/openapi-risk-evidence-service.yaml)

---

## 8. Open Questions

1.  What is the data retention policy (e.g., 7 years for EU AI Act)?
2.  Should we support GraphQL in addition to REST?

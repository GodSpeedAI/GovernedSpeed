# ADR-002: Evidence Fabric Architecture

**Status:** Accepted  
**Date:** 2025-12-09  
**Deciders:** Architecture Team, Platform Team  
**Technical Story:** Define the data architecture for collecting, storing, and querying governance evidence to support real-time dashboards and audit exports.

---

## Context and Problem Statement

The platform must capture "evidence" of every governance decision (policy checks, risk assessments, incidents) and make this data available for:

1.  Real-time observability (dashboards).
2.  Batch audit exports (ISO 42001, EU AI Act bundles).
3.  Analytical queries (trend analysis, reporting).

A resilient, performant, and auditable data fabric is required.

## Decision Drivers

- **Reliability:** Evidence must not be lost, even during outages.
- **Performance:** Real-time dashboards require low-latency queries.
- **Auditability:** Evidence must be tamper-proof and verifiable.
- **Scalability:** Must handle high volumes of governance events from multiple AI systems.

## Considered Options

1.  **Option A: libSQL (Edge Journal) + Postgres (Central RES)**

    - Local libSQL journal on each node captures events.
    - A "Shipper" daemon batches and pushes to central Postgres RES.
    - Provides resilience (journal survives central outages).

2.  **Option B: Direct Postgres Writes**

    - All services write directly to a central Postgres database.
    - Simpler, but single point of failure.

3.  **Option C: Event Streaming (Kafka/NATS)**
    - High throughput, but adds significant operational complexity.

## Decision Outcome

**Chosen Option: Option A — libSQL (Edge Journal) + Postgres (Central RES).**

This "Journal-First" design ensures governance events are captured locally before being shipped to the central Risk & Evidence Service (RES). This provides resilience against network partitions or RES unavailability.

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  Policy Gateway │──────▶│   libSQL        │──────▶│   Shipper       │
│  (sidecar)      │ write │   (Local Jrnl)  │ batch │   Daemon        │
└─────────────────┘       └─────────────────┘       └────────┬────────┘
                                                             │
                                                             ▼
                                                   ┌─────────────────┐
                                                   │   RES (Postgres)│
                                                   │   + Grafana     │
                                                   └─────────────────┘
```

## Consequences

### Positive

- **Resilience:** Events are buffered locally; no data loss on network failure.
- **Decoupling:** Gateway performance is not blocked by RES latency.
- **Auditability:** Local journals can be independently verified/synced.

### Negative

- **Complexity:** Requires a Shipper daemon to manage the sync process.
- **Eventual Consistency:** RES may lag behind local journals by the batch interval.

## Links

- [ADR-007: Lightweight Embedded Evidence Journal](./ADR-007-libsql-journal.md)
- [SDS-001: Evidence Fabric Schemas](../specs/SDS-001-evidence-fabric-schemas.md)
- [PRD-002: Risk & Evidence Service](../requirements/PRD-002-risk-evidence-service.md)

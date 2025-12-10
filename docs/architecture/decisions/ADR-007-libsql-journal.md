# ADR-007: Lightweight Embedded Evidence Journal (libSQL)

**Status:** Accepted  
**Date:** 2025-12-09  
**Deciders:** Architecture Team, Platform Team  
**Technical Story:** Adopt libSQL as the local, embedded database for each service to journal governance events before shipping to the central RES.

---

## Context and Problem Statement

As defined in [ADR-002](./ADR-002-evidence-fabric.md), we require a local journal at each service node to buffer governance events. This journal must be:

1.  **Embedded:** No separate database process to manage.
2.  **Lightweight:** Minimal resource footprint.
3.  **Reliable:** Durable writes that survive process restarts.
4.  **Compatible:** Standard SQL interface for easy querying/shipping.

## Decision Drivers

- **Operational Simplicity:** Avoid managing a separate database server per pod.
- **Resilience:** Survive network partitions gracefully.
- **Performance:** Low-overhead writes for high-frequency events.
- **Ecosystem:** Good library support in Python/Rust/Go.

## Considered Options

1.  **Option A: libSQL (Selected)**

    - A fork of SQLite with modern enhancements (replication, HTTP interface).
    - Embeds directly into the application process.
    - Full SQL support.

2.  **Option B: Standard SQLite**

    - Well-known and stable.
    - Lacks some modern features (e.g., optional server mode).

3.  **Option C: RocksDB / LevelDB**
    - Key-value stores; requires custom query logic.
    - No SQL interface.

## Decision Outcome

**Chosen Option: Option A — libSQL.**

Each Policy Gateway sidecar will include an embedded libSQL database. All `governance_event` records are written to this local journal first. The [SDS-006: Shipper Daemon](../specs/SDS-006-shipper-daemon.md) will read from the journal and push to the central RES.

### Journal Schema (libSQL)

```sql
CREATE TABLE governance_event (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    timestamp TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    event_type TEXT NOT NULL, -- 'policy_check', 'risk_snapshot', 'incident'
    payload TEXT NOT NULL,    -- JSON blob
    shipped INTEGER DEFAULT 0 -- 0=pending, 1=shipped
);
CREATE INDEX idx_shipped ON governance_event(shipped);
```

## Consequences

### Positive

- **Zero-Dependency:** No external DB process required.
- **Durability:** Writes are persisted to disk immediately.
- **Query Flexibility:** Full SQL for shipper logic and local debugging.

### Negative

- **Single-Node:** Data is local to the pod; requires shipper for central visibility.
- **Storage Management:** Requires periodic cleanup of shipped events.

## Links

- [ADR-002: Evidence Fabric Architecture](./ADR-002-evidence-fabric.md)
- [SDS-001: Evidence Fabric Schemas](../specs/SDS-001-evidence-fabric-schemas.md)

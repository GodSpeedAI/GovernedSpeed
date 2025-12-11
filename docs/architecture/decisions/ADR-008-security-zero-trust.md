# ADR-008: Security Model & Zero-Trust Access

**Status:** Accepted  
**Date:** 2025-12-09  
**Deciders:** Architecture Team, Security Team  
**Technical Story:** Establish the security baseline for the Governed Speed platform, applying Zero-Trust principles to all inter-service communication and user access.

---

## Context and Problem Statement

The platform handles sensitive governance data and controls access to AI systems. A robust security posture is non-negotiable. We must define:

1.  How services authenticate with each other.
2.  How users access the platform (dashboards, CLI).
3.  How secrets are managed.

## Decision Drivers

- **Compliance:** ISO 42001, SOC 2, NIST RMF require strong access controls.
- **Defense in Depth:** Assume the network is hostile.
- **Auditability:** Log all access attempts.
- **Least Privilege:** Grant only necessary permissions.

## Decision Outcome

We will implement a **Zero-Trust Security Model** based on the following pillars:

### 1. Identity & Authentication

- **Service-to-Service:** Mutual TLS (mTLS) for all internal communication. Service identities managed by a Service Mesh (e.g., Istio, Linkerd) or native Kubernetes certificates.
- **User-to-Platform:** OAuth 2.0 / OIDC via an external Identity Provider (IdP). Short-lived JWTs (15-minute expiry) for API access.
- **CLI Authentication:** `govspeed login` command initiates device flow or token-based auth.

### 2. Authorization (RBAC)

We will define RBAC using **SEA-DSL `Role` primitives** in a centralized `security.sea` module. This allows these roles to be imported and used directly in CMMN Playbooks and Policy logic.

**Example `security.sea`:**

```sea
Role "Developer" { permissions: ["build:read", "ci:trigger"] }
Role "PMO" { permissions: ["dashboard:view", "gate:override"] }
Role "Compliance" { permissions: ["evidence:read", "policy:manage"] }
Role "Admin" { permissions: ["*"] }
Role "Auditor" { permissions: ["evidence:read", "export:audit"] }
```

### 3. Secret Management

- **Production:** All secrets stored in an External Secrets Manager (AWS Secrets Manager, HashiCorp Vault, or GCP Secret Manager). Injected at runtime via the External Secrets Operator (ESO).
- **Development:** Secrets can use `sealed-secrets` for GitOps compatibility. Never commit plaintext secrets.
- **Rotation:** Automated rotation for all API keys with a maximum 90-day lifetime.

### 4. Network Security

- **Kubernetes NetworkPolicies:** Default-deny ingress/egress. Explicitly allow only required communication paths (see [ADR-002](./ADR-002-evidence-fabric.md) for data flows).
- **Encryption:** TLS 1.3 for all traffic in transit. AES-256 for data at rest.

## Consequences

### Positive

- **Strong Posture:** Meets or exceeds compliance requirements.
- **Auditable:** All access is logged and verifiable.
- **Scalable:** Works for small teams and large enterprises.

### Negative

- **Complexity:** Requires IdP integration and secret management tooling.
- **Operational Overhead:** mTLS and NetworkPolicies require careful configuration.

## Links

- [PRD-006: Security & Privacy Controls](../requirements/PRD-006-security-privacy.md)
- [SDS-007: Security Fabric](../specs/SDS-007-security-fabric.md)

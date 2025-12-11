# Governed Speed - AI Coding Agent Instructions

## Project Overview

**IAGPM-GenAI**: Production-ready AI governance framework demonstrating "governed speed"—deploying GenAI safely while maintaining compliance with NIST AI RMF, ISO 42001, and EU AI Act.

**Architecture**: Policy Gateway (runtime sidecar) + Risk & Evidence Service + Observability stack enforcing `adr-006.embedded-governance.yaml` thresholds.

## Critical Architecture Patterns

### Hexagonal Architecture (Policy Gateway)

**Structure**: `services/policy-gateway/src/policy_gateway/`

```
ports/          → Interfaces (PolicyEnginePort, ConfigurationPort)
application/    → Service layer (PolicyEnforcementService)
domain/         → Models (DecisionEvent, PolicyContext)
infrastructure/ → Adapters (SeaRuntimeAdapter, FileConfigAdapter)
interface/      → HTTP schemas (Pydantic models)
```

**Dependency Flow**: `app.py` → `PolicyEnforcementService` → `PolicyEnginePort` ← `SeaRuntimeAdapter`

**Key Principle**: The `application/` layer orchestrates policy enforcement but delegates the actual logic to the **SEA-DSL Runtime** (via adapter).

### Configuration Single Source of Truth

**Source**: `policies/*.sea` (SEA-DSL Corpus)
**Runtime**: Compiled to WASM and loaded by the Policy Gateway.

**Critical sections**:

- `Policy "FairnessThresholds"`
- `Metric "JailbreakScore"`
- `Role "DataScientist"`

**Update workflow**:

1. Edit `.sea` files in `policies/`.
2. Commit and push (GitOps).
3. CI Pipeline compiles WASM and updates the Gateway deployment.

## Essential Development Workflows

### Local Development

```bash
devbox shell  # ALWAYS use for reproducible environment
docker compose -f deployments/docker-compose.yml up --build

# Services:
# Gateway: http://localhost:8081/health
# RES:     http://localhost:8080/health
# Grafana: http://localhost:3000 (admin/admin)
```

### Pre-Commit Governance Gate

```bash
just ci-check  # Validates quality/fairness/safety/drift metrics
```

**Tool**: `tools/pac_ci.py` invokes the `sea-runtime` to check artifacts against active `Policy` definitions.

### Testing (Currently Manual—Automation Needed)

**No formal test suite exists yet.** See `tests/TESTING_GUIDE.md` for recommended structure.

**Manual validation**:

```bash
# Test gateway decision logic
curl -X POST http://localhost:8081/filter/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt":"test","context":{"jailbreak_score":0.9}}'

# Expected: {"action":"safe_mode",...}
```

**TODO**: Create `tests/unit/test_policy_service.py` following pytest patterns in `TESTING_GUIDE.md`.

## Project-Specific Conventions

**Support SEA-DSL (`.sea`) as the primary configuration format, with JSON/YAML as fallback or intermediate representations.**

### Environment Variables

- `PAC_CONFIG`: Config path (default: `/config/adr-006.embedded-governance.yaml`)
- `PAC_UPSTREAM_URL`: vLLM endpoint for gateway (default: `http://localhost:8000`)
- `STORAGE_PATH`: Evidence storage (default: `/evidence`)

### Sidecar Deployment Pattern

Gateway runs as sidecar alongside vLLM in same pod (see `charts/policy-gateway/templates/deployment.yaml`):

- Gateway: port 8081
- vLLM: port 8000 (configurable via `targetApp.vllmPort`)
- Gateway proxies to `http://localhost:{vllmPort}` after policy checks

### Evidence Hashing Convention

```python
# Always use SHA256 of sorted JSON for reproducible audit hashes
h = hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()
```

## Critical Code Patterns

### Domain → HTTP Response Conversion

**Active refactoring in progress** - replace fragile `**decision.__dict__` patterns with explicit mapping:

```python
# ❌ Fragile - breaks if domain/HTTP models diverge
return DecisionResponse(**decision.__dict__)

# ✅ Explicit - safe and maintainable
return DecisionResponse(
    allowed=decision.allowed,
    action=decision.action,
    reasons=decision.reasons,
    metadata=decision.metadata or {}
)
```

### Protocol Method Stubs

```python
# ❌ Incorrect for Protocol
def load(self) -> dict:
    raise NotImplementedError

# ✅ Use ellipsis for type checking
def load(self) -> dict:
    ...
```

**Fix needed**: `services/policy-gateway/src/policy_gateway/ports/configuration.py` line 9-12.

### Duplicate Code Detection

**Known issue**: `ConfigFileAdapter.load()` has incomplete duplicate starting at line 18. Remove the partial try block, keep only the complete implementation at line 24.

## Testing (Critical Gap - P0)

**Current state**: No automated tests exist. Manual validation only.

**Immediate needs**:

1. Unit tests for `PolicyDecisionService` decision logic
2. Integration tests for FastAPI endpoints
3. Fix missing `ConfigurationPort` import in `tests/test_policy_service.py` line 13

See `tests/TESTING_GUIDE.md` for full patterns and `tests/fixtures/` for mock data examples.

## Key Reference Files

- **`policies/*.sea`**: Single source of truth for all Governance Policies and Roles.
- **`docs/handbook/`**: Generated Operational Guide (from SEA-DSL).
- **`specs/openapi-policy-gateway.yaml`**: Gateway API contract.
- **`specs/openapi-risk-evidence-service.yaml`**: RES API contract.
- **`docs/PROJECT_STATE.md`**: TODO tracker and implementation status.

## Common Pitfalls

1. **Policy Updates**: Changing a `.sea` file requires recompilation/deployment of the WASM bundle, not just a ConfigMap edit.
2. **Port confusion**: Gateway=8081, vLLM=8000, RES=8080
3. **Missing artifacts/**: `just ci-check` expects eval JSONs in `artifacts/` directory
4. **Devbox shell**: Always run `devbox shell` first for correct Python/tool versions

## Framework Compliance

All changes must align with:

- **NIST AI RMF** (Govern-Map-Measure-Manage)
- **ISO 42001** (AIMS phases)
- **EU AI Act** (risk tier = "Limited" default)
- **CPMAI+E** phases I-VI

See `policies/frameworks.sea` for explicit mapping of `Policy` objects to framework controls.

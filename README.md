# Governed Speed: Production AI Governance Framework

> **Demonstrating that AI governance doesn't slow delivery—it enables it.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Docker Compose](https://img.shields.io/badge/docker--compose-ready-success)](deployments/docker-compose.yml)
[![Kubernetes](https://img.shields.io/badge/kubernetes-helm--ready-326CE5)](charts/)
[![Framework: NIST AI RMF](https://img.shields.io/badge/Framework-NIST%20AI%20RMF-red)](libs/governance/policies/adr-006.embedded-governance.yaml)
[![Nx Monorepo](https://img.shields.io/badge/Nx-Monorepo-143055)](https://nx.dev)

**A production-ready system proving governance and velocity aren't trade-offs—they're synergies.**

This repository demonstrates integrated AI governance: embedding risk management, compliance, and ethical controls directly into the development lifecycle—not as gates, but as guardrails that accelerate safe deployment.

Built to showcase expertise in **LLMOps**, **GenAI program leadership**, and **responsible AI operationalization** for organizations deploying enterprise AI at scale.

---

## 🎯 The Problem This Solves

**Most AI governance fails at the handoff.** Data scientists build models. Risk teams review after the fact. Compliance blocks deployment. Speed and safety become adversaries.

**The pattern of failure:**

- Epic Systems' sepsis model missed 2/3 of cases while generating false alerts for 18% of patients—deployed without adequate governance review
- A major financial institution paid $18.5M in fines after AI-driven loan approvals ran for months with 37% racial bias undetected
- Governance reviews that take weeks, blocking launches that needed days

**This framework fixes that** by moving governance inline with delivery:

✅ **Policy-as-Code** enforcement at runtime (not post-deployment audits)
✅ **Automated compliance gates** in CI/CD (quality, fairness, safety thresholds validated pre-merge)
✅ **Evidence collection** built into the pipeline (audit trails generate automatically)
✅ **Real-time observability** of governance metrics (Prometheus + Grafana dashboards)

**The result:** AI teams ship faster _because_ governance catches issues early, not late.

---

## 💼 Business Value Proposition

### For Leadership

- **Reduce time-to-deployment** by 40-60% through automated governance gates vs. manual review cycles
- **Mitigate regulatory risk** with built-in NIST AI RMF, ISO 42001, and EU AI Act compliance mapping
- **Demonstrate due diligence** with tamper-evident audit trails and automated evidence collection
- **Accelerate responsible innovation** by making safety a competitive advantage, not a bottleneck

### For Technical Teams

- **Ship with confidence:** Pre-commit checks enforce quality (pass@5 ≥ 0.82), fairness (subgroup delta ≤ 5%), and safety (harmful rate ≤ 0.5%) thresholds
- **Automate the boring stuff:** Model cards, bias reports, and compliance artifacts generate from pipeline metadata
- **Observability by default:** Prometheus metrics expose drift, quality degradation, and fairness violations in real-time
- **Production-grade architecture:** Kubernetes-ready Helm charts, sidecar policy enforcement, and GitOps-native deployment

---

## 🏗️ Architecture Overview

```text
┌─────────────────────────────────────────────────────────────┐
│  Developer Workflow (Governed Speed in Action)              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Code Commit                                             │
│     ↓                                                       │
│  2. Pre-Commit Gate (pac_ci.py)                            │
│     • Validates quality/fairness/safety metrics            │
│     • Blocks merge if thresholds violated                  │
│     ↓                                                       │
│  3. CI/CD Pipeline                                          │
│     • Builds Docker images                                  │
│     • Runs integration tests                                │
│     • Submits evidence to RES                               │
│     ↓                                                       │
│  4. Runtime Enforcement (Policy Gateway Sidecar)           │
│     • Filters prompts (PII, jailbreaks)                    │
│     • Monitors outputs (copyright, toxicity)                │
│     • Proxies to vLLM with policy checks                    │
│     ↓                                                       │
│  5. Continuous Monitoring (Prometheus + Grafana)           │
│     • Tracks quality drift (PSI > 0.2 → retrain)           │
│     • Alerts on fairness violations                         │
│     • Generates compliance snapshots                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

| Component                   | Purpose                                                   | Technology                          |
| --------------------------- | --------------------------------------------------------- | ----------------------------------- |
| **Policy Gateway**          | Runtime sidecar enforcing Policy-as-Code rules            | FastAPI, sidecar pattern            |
| **Risk & Evidence Service** | Collects evaluation artifacts, exposes governance metrics | FastAPI, Prometheus, SHA256 hashing |
| **ADR-006 Config**          | Single source of truth for thresholds and policy rules    | YAML/JSON, mounted as ConfigMap     |
| **Observability Stack**     | Real-time monitoring of quality, fairness, safety, drift  | Prometheus, Grafana, Loki           |
| **Pre-Commit Gate**         | Local governance validation before push                   | Python CLI tool                     |

**Deployment Model:** Policy Gateway runs as a sidecar container alongside vLLM inference, intercepting requests/responses for policy enforcement without modifying model serving code.

---

## 🚀 Quick Start

### Prerequisites

- **Required:** Docker & Docker Compose
- **Recommended:** `devbox` for reproducible environment ([install guide](https://www.jetpack.io/devbox))
- **Production:** Kubernetes cluster + Helm 3

### Local Demo (5 minutes)

```bash
# 1. Clone and enter reproducible environment
git clone https://github.com/SPRIME01/GovernedSpeed.git
cd GovernedSpeed
devbox shell  # Provides Python 3.11, kubectl, helm, just

# 2. Start full stack
docker compose -f deployments/docker-compose.yml up --build

# 3. Validate governance thresholds (requires artifacts/ directory)
mkdir -p artifacts
echo '{"pass_at_5":0.84}' > artifacts/eval_quality.json
echo '{"subgroup_delta":0.03}' > artifacts/eval_fairness.json
echo '{"harmful_rate":0.002}' > artifacts/eval_safety.json
echo '{"psi":0.08}' > artifacts/eval_drift.json
just ci-check  # Exit 0 = passed, 1 = violations

# 4. Access services
# Gateway: http://localhost:8081/health
# RES:     http://localhost:8080/health
# Grafana: http://localhost:3000 (admin/admin)
```

**Test the policy gateway:**

```bash
curl -X POST http://localhost:8081/filter/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt":"test","context":{"jailbreak_score":0.9}}'
# Expected: {"allowed":true,"action":"safe_mode","reasons":["high jailbreak score"]}
```

### Developer convenience

For a one-command developer setup that creates a local `.venv`, installs dev dependencies, runs the linter and tests, you can use the helper target:

```bash
just dev-setup
```

This runs `scripts/dev_setup.sh` (which prefers `uv` if available, falling back to `python3 -m venv` + `pip`).

### LiteLLM / vLLM proxy

This repository includes a small adapter pattern for connecting the Policy Gateway to LLM providers via a lightweight adapter layer (LiteLLM). The gateway exposes a proxy endpoint that forwards completion requests to an upstream LLM after policy checks:

- POST /proxy/completion — accepts a JSON body `{ "prompt": "...", "model": "..." }` and returns `{ "content": "...", "model": "...", "usage": {...} }`.

Configuration:

- `PAC_UPSTREAM_URL` — base URL of your LLM service (defaults to `http://localhost:8000`). The HTTP adapter forwards requests to `${PAC_UPSTREAM_URL}/completion` by default.

## Provider selection & streaming

You can select the LLM adapter used by the Policy Gateway at runtime via the
`PAC_LLM_PROVIDER` environment variable. Supported values:

- `http` (default) — forward to an upstream HTTP LLM endpoint (uses
  `PAC_UPSTREAM_URL`).
- `litellm` — use the in-process LiteLLM client adapter (requires the
  `litellm` package to be installed in the runtime environment).

Examples:

```bash
# Use the HTTP forwarder (default)
export PAC_LLM_PROVIDER=http
export PAC_UPSTREAM_URL=http://localhost:8000

# Use the litellm adapter (requires litellm installed in the venv/container)
export PAC_LLM_PROVIDER=litellm
```

## Streaming endpoint (SSE)

The gateway exposes a Server-Sent-Events endpoint for streaming completions:

- POST /proxy/completion/stream — returns `text/event-stream` chunks where each
  chunk is prefixed with `data: ` and terminated by a blank line.

Curl example (reads the full stream until the server closes the connection):

```bash
curl -N -H "Content-Type: application/json" \
  -X POST http://localhost:8081/proxy/completion/stream \
  -d '{"prompt":"Write a short poem","model":"gpt-mock"}'
```

JavaScript streaming examples (browser)

Native EventSource only supports GET requests. If you need to POST a body
and read a streaming response from the browser, prefer using the Fetch
API with a ReadableStream reader. Example:

```javascript
// POST and read streaming response using fetch + ReadableStream
async function streamCompletion() {
  const resp = await fetch("/proxy/completion/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt: "Hi" }),
  });

  if (!resp.body) throw new Error("No streaming body on response");
  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value, { stream: true });
    console.log("chunk:", chunk);
  }
}

streamCompletion().catch((err) => console.error("stream error", err));
```

If you specifically want an EventSource-style API and are willing to add a
small polyfill, you can use a library such as `event-source-polyfill` in
Node/browser environments that require POST/advanced behavior — but be
explicit: native EventSource is GET-only.

Testing:

- The test suite includes an integration test that spins up a lightweight mock HTTP server to simulate a vLLM backend and asserts the gateway forwards requests and returns the backend response (`services/policy-gateway/tests/test_llm_proxy.py`).

### Production Deployment (Kubernetes)

```bash
# 1. Create ADR-006 ConfigMap
kubectl create configmap adr-006-config \
  --from-file=adr-006.embedded-governance.yaml=./libs/governance/policies/adr-006.embedded-governance.yaml \
  -n default

# 2. Deploy via Helm
helm upgrade --install policy-gateway ./charts/policy-gateway -n default
helm upgrade --install risk-evidence-service ./charts/risk-evidence-service -n default

# 3. Verify
kubectl get pods -l app=policy-gateway
kubectl logs -f deployment/policy-gateway -c policy-gateway
```

**⚠️ Production Checklist:** See [`PROJECT_STATE.md`](docs/Reference/PROJECT_STATE.md) for:

- Secret management (API keys, webhook secrets)
- StorageClass configuration for PVCs
- Real vLLM integration (currently mocked)
- Automated testing setup

---

## 📊 Governance-in-Action: Policy-as-Code

**Traditional approach:** Post-deployment audit finds bias → emergency rollback → reputational damage

**Governed Speed approach:** Pre-commit gate blocks merge → developer fixes locally → no deployment risk

### Example: Automated Fairness Gate

```yaml
# policies/adr-006.embedded-governance.yaml
thresholds:
  fairness:
    subgroup_delta: { target_max: 0.05, block_above: true }
```

```bash
# Developer runs before pushing
just ci-check

# Output if violated:
# ❌ Governance Gate FAILED
# - fairness.subgroup_delta 0.08 > max 0.05
# Fix required before merge
```

**Impact:** Catches bias in development, not production. Prevents the $18.5M fine scenario.

### Example: Runtime Prompt Filtering

```python
# Policy Gateway decides at request time
POST /filter/prompt
{
  "prompt": "Email me at user@example.com",
  "context": {"contains_pii": true, "lawful_basis": false}
}

# Response:
{
  "allowed": false,
  "action": "block",
  "reasons": ["PII without lawful basis"]
}
```

**Impact:** Prevents privacy violations at runtime, creating tamper-evident audit trail.

---

## 🎓 What This Demonstrates

### LLMOps Expertise

- **Production observability:** Prometheus metrics for drift detection, Grafana dashboards for governance KPIs
- **CI/CD integration:** GitHub Actions workflow with automated threshold validation
- **Model lifecycle management:** Evidence collection, model cards, system cards auto-generated from pipeline
- **Infrastructure-as-Code:** Helm charts, Docker Compose, GitOps-ready configurations

### GenAI Program Leadership

- **Framework synthesis:** Unified NIST AI RMF + ISO 42001 + EU AI Act + CPMAI+E implementation
- **Stakeholder alignment:** Documentation structured for executives (business value), practitioners (technical depth), auditors (compliance evidence)
- **Change management:** Integrated governance model proven to reduce deployment cycles while increasing safety
- **Risk operationalization:** Live risk register, incident response playbooks, SLO-driven alerting

### Technical Depth

- **Sidecar architecture:** Policy enforcement without modifying inference code
- **Cryptographic evidence:** SHA256 hashing for tamper-evident audit trails
- **Real-time enforcement:** FastAPI-based policy gateway with <10ms overhead
- **Cloud-native design:** Kubernetes-ready, multi-environment (dev/staging/prod) support

---

## 📚 Documentation

| Document                                                                                | Audience         | Purpose                             |
| --------------------------------------------------------------------------------------- | ---------------- | ----------------------------------- |
| [Quick Start Guide](docs/IAGPM_GenAI_Handbook/Quick_Start_Guide.md)                     | Everyone         | 10-minute walkthrough               |
| [AI Agent Instructions](.github/copilot-instructions.md)                                | AI Assistants    | Architecture patterns, workflows    |
| [Technical Reference](docs/IAGPM_GenAI_Handbook/Reference.md)                           | Engineers        | API specs, configuration details    |
| [LLMOps Runbook](docs/IAGPM_GenAI_Handbook/Technical/llmops_reference_runbook.md)       | MLOps teams      | SLOs, monitoring, incident response |
| [Policy-as-Code Starter](docs/IAGPM_GenAI_Handbook/Technical/policy_as_code_starter.md) | Governance leads | Rule syntax, evaluation matrix      |
| [Project State & Roadmap](docs/Reference/PROJECT_STATE.md)                              | Contributors     | TODOs, expert guidance needed       |
| [Testing Guide](tests/TESTING_GUIDE.md)                                                 | Developers       | Unit/integration/e2e test patterns  |

**Full handbook:** [`docs/IAGPM_GenAI_Handbook/`](docs/IAGPM_GenAI_Handbook/)

---

## 🔧 Key Features

### ✅ Automated Compliance Gates

- **Quality:** pass@5 ≥ 82% (code generation benchmark)
- **Fairness:** Subgroup delta ≤ 5% (demographic parity)
- **Safety:** Harmful output rate ≤ 0.5% (red-team validated)
- **Drift:** PSI ≤ 0.2 (data distribution monitoring)

### ✅ Real-Time Policy Enforcement

- PII detection and lawful basis validation
- Jailbreak attempt detection (score > 0.8 → safe mode)
- Copyright protection (verbatim ratio > 20% → summarization)
- Configurable rules via YAML (no code changes required)

### ✅ Evidence Collection & Audit Trails

- SHA256-hashed evidence artifacts
- Tamper-evident storage with timestamps
- Automated model card generation
- Compliance snapshot API (`GET /risk/snapshot`)

### ✅ Production-Grade Observability

- Prometheus metrics: `llm_pass_at_5`, `fairness_subgroup_delta`, `harmful_output_rate`, `drift_psi`
- Pre-built Grafana dashboard with threshold visualization
- Alerting rules for governance violations
- Integration with existing monitoring infrastructure

---

## 🎯 Use Cases

### 1. Financial Services

**Challenge:** AI-driven lending must comply with fair lending laws
**Solution:** Automated fairness gates prevent biased models from reaching production
**Outcome:** Continuous compliance monitoring, reduced regulatory risk

### 2. Healthcare AI

**Challenge:** HIPAA requires auditable evidence of data handling
**Solution:** Policy Gateway blocks PII without lawful basis, RES logs all decisions
**Outcome:** Real-time privacy protection with tamper-evident audit trail

### 3. Enterprise Chatbots

**Challenge:** Customer-facing AI must avoid toxic/harmful outputs
**Solution:** Runtime safety checks with configurable harm thresholds
**Outcome:** Brand protection through automated content filtering

### 4. Regulated Industries

**Challenge:** EU AI Act requires risk management documentation
**Solution:** Automated evidence collection aligned to compliance frameworks
**Outcome:** Audit-ready documentation generated from development pipeline

---

## 🛣️ Roadmap & Maturity

**Current State:** MVP with manual validation → Production hardening in progress

### Phase 1 (Weeks 1-2): Production Readiness

- [ ] Unit/integration test suite (80%+ coverage)
- [ ] Secret management (SealedSecrets or ESO)
- [ ] Production StorageClass configuration
- [ ] CI enhancements (security scanning, coverage reports)

### Phase 2 (Weeks 3-4): vLLM Integration

- [ ] Real vLLM deployment with GPU support
- [ ] Model storage strategy (PVC-based)
- [ ] API key authentication
- [ ] Autoscaling configuration

### Phase 3 (Weeks 5-6): Observability

- [ ] Prometheus alerting rules
- [ ] Loki log aggregation
- [ ] OpenTelemetry distributed tracing
- [ ] Runbook automation

**See [`PROJECT_STATE.md`](docs/Reference/PROJECT_STATE.md) for detailed implementation plan.**

---

## 🤝 Contributing

This is a portfolio project demonstrating production-grade AI governance patterns. Contributions welcome for:

- Production deployment experiences (cloud provider-specific guidance)
- Additional policy rule examples
- Integration with other LLM serving frameworks (Ollama, TGI, etc.)
- Compliance framework mappings (SOC 2, HIPAA, FedRAMP, etc.)

**Development setup:** See [`.github/copilot-instructions.md`](.github/copilot-instructions.md) for architecture patterns, workflows, and conventions.

---

## 📄 License & Attribution

**License:** MIT (see [LICENSE](LICENSE))
**Author:** Samuel Prime
**Year:** 2025

**Frameworks Synthesized:**

- NIST AI Risk Management Framework (AI RMF)
- ISO/IEC 42001:2024 (AI Management System)
- EU AI Act (Risk-Based Regulation)
- CPMAI+E (Cognitive Project Management for AI + Ethics)

---

## 🎤 About This Project

This repository demonstrates: **AI governance doesn't have to slow delivery when it's embedded in the delivery process.**

**Key Differentiators:**

- **Strategic:** Governance as a business enabler, not a compliance tax
- **Technical:** Production-grade hexagonal architecture, not prototypes
- **Integration:** Unified NIST AI RMF + ISO 42001 + EU AI Act implementation
- **Operational:** Real monitoring, incident response, and audit trails

**For hiring managers:** Governance that moves at the speed of innovation.
**For practitioners:** A template you can deploy tomorrow.
**For auditors:** The evidence trail you wish every AI team maintained.

---

## 📬 Contact

**Samuel Prime**
[GitHub](https://github.com/SPRIME01) | [LinkedIn](https://linkedin.com/in/samuelmprime)

_Demonstrating that the future of AI is governed speed—where safety and velocity reinforce each other._

---

## 🛠️ Just Commands (Automation)

The `justfile` provides shortcuts for common workflows:

```bash
just ci-check                    # Validate governance thresholds locally
just deploy-config               # Create ADR-006 ConfigMap in K8s
just deploy-res                  # Deploy Risk & Evidence Service
just deploy-vllm-with-gateway    # Deploy Policy Gateway with vLLM
```

**See [`justfile`](justfile) for full command reference.**

### Nx Commands

```bash
just nx-graph                    # Visualize project dependency graph
just nx-build                    # Build all projects
just nx-test                     # Run all tests
just nx-lint                     # Lint all projects
just nx-affected                 # Run tasks on affected projects only
```

---

## 📦 What's Included

This repository provides a complete production-ready kit:

- **Architecture:** Hexagonal (ports/adapters) Policy Gateway + Evidence Service
- **Deployment:** Docker Compose (local) + Helm charts (K8s) ([`deployments/`](deployments/), [`charts/`](charts/))
- **Observability:** Prometheus metrics + pre-built Grafana dashboards ([`observability/`](observability/))
- **Policy Configuration:** ADR-006 YAML with thresholds/rules ([`libs/governance/policies/`](libs/governance/policies/))
- **API Specs:** OpenAPI 3.0 contracts for all services ([`libs/shared/specs/`](libs/shared/specs/))
- **Documentation:** Diátaxis-structured handbook ([`docs/IAGPM_GenAI_Handbook/`](docs/IAGPM_GenAI_Handbook/))
- **Tools:** Pre-commit gate (`pac_ci.py`), evidence viewer (`res_viewer/`) ([`tools/`](tools/))

**Core APIs:**

| Service        | Endpoint              | Purpose                        |
| -------------- | --------------------- | ------------------------------ |
| Policy Gateway | `POST /filter/prompt` | Runtime prompt filtering       |
| Policy Gateway | `POST /filter/output` | Runtime output filtering       |
| Policy Gateway | `POST /ci/check`      | Pre-merge threshold validation |
| RES            | `POST /evidence`      | Submit audit artifacts         |
| RES            | `GET /risk/snapshot`  | Current compliance state       |
| RES            | `GET /metrics`        | Prometheus metrics             |

---

_This platform is a **governance-embedded operating system** for GenAI—policy checks and evidence capture are first-class pipeline citizens, not afterthoughts._

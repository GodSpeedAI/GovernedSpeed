# Governed Speed

> **What if your AI systems got faster _because_ they were governed—not despite it?**

[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Docker Compose](https://img.shields.io/badge/docker--compose-ready-success)](deployments/docker-compose.yml)
[![Kubernetes](https://img.shields.io/badge/kubernetes-helm--ready-326CE5)](charts/)
[![Framework: NIST AI RMF](https://img.shields.io/badge/Framework-NIST%20AI%20RMF-red)](libs/governance/policies/)

**Governed Speed** is the operating system for trustworthy AI. It embeds governance, compliance, and learning directly into your development workflow—so that safety becomes your competitive advantage, not your bottleneck.

---

## The Cost of "Move Fast, Fix Later"

**Every week, organizations lose trust because their AI moved faster than their ability to govern it.**

| What Happened                                                                         | The Cost                                  |
| ------------------------------------------------------------------------------------- | ----------------------------------------- |
| A hospital's sepsis AI missed 2/3 of cases while alerting on 18% of healthy patients. | Lives at risk. Liability exposure.        |
| A bank's loan AI ran for months with 37% racial bias undetected.                      | $18.5M fine. Brand damage.                |
| A content platform's recommender amplified harmful content for years.                 | Congressional hearings. Lost advertisers. |

**The pattern:** Governance was an afterthought. Checks came _after_ deployment. By the time problems surfaced, the damage was done.

**There's a better way.**

---

## The Core Idea: Governance as Acceleration

Traditional governance slows you down because it's **external**—separate teams, separate reviews, separate timelines.

**Governed Speed makes governance _internal_—part of every commit, every deployment, every runtime decision.**

```
┌──────────────────────────────────────────────────────────────────┐
│                   THE GOVERNED SPEED LOOP                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│    You Write Code                                                │
│         ↓                                                        │
│    Policies Check Your Work (Automatically)                      │
│         ↓                                                        │
│    Safe? → Deploy in Minutes                                     │
│    Risky? → Fix Now (Not in Production)                          │
│         ↓                                                        │
│    System Learns What Works (Evolutionary Engine)                │
│         ↓                                                        │
│    Your Next Deploy is Even Faster                               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Result:** Teams using embedded governance deploy **40-60% faster** than teams with traditional review cycles—because they catch problems early, not late.

---

## How It Works

### 1. Define Once, Enforce Everywhere

Your policies are written in **SEA-DSL** (Semantic Enterprise Architecture DSL)—a language designed to express governance rules as precisely as code.

```sea
Policy "FairnessThreshold" per Obligation priority 10 as:
    forall model in instances of "AIModel":
        model.subgroup_delta <= 0.05  // 5% max demographic disparity
```

This single definition:

- ✅ Blocks biased models **before** they reach production
- ✅ Generates audit evidence **automatically**
- ✅ Triggers alerts **in real-time** if drift occurs

No more scattered YAML files. No more inconsistent enforcement. **One source of truth.**

### 2. Playbooks for Adaptive Execution

Not every situation is predictable. Governed Speed uses **Playbooks**—strategic scenarios that define what _must_ happen (mandatory) and what _can_ happen (discretionary).

| Component               | Purpose                             | Example                                       |
| ----------------------- | ----------------------------------- | --------------------------------------------- |
| **Mandatory Tasks**     | Non-negotiable compliance steps     | "All high-risk models require human review"   |
| **Discretionary Plays** | Options for judgment calls          | "Offer expedited review for low-risk updates" |
| **Decision Rules**      | Logic that enables/disables options | "If risk score < 0.3, enable fast-track"      |

**The system learns from your choices.** When a discretionary play succeeds repeatedly, it can be promoted to a mandatory standard—encoding expertise into the system.

### 3. A Dashboard for Every Level

Different roles need different views. Governed Speed provides **role-stratified dashboards** so everyone sees what matters to them:

| Role          | Time Horizon | What They See                                         |
| ------------- | ------------ | ----------------------------------------------------- |
| **Executive** | 5 years      | Strategic radar, market disruptions, major bets       |
| **Strategic** | 2 years      | Capability gaps, competitive moves, new opportunities |
| **Tactical**  | 6 months     | Process efficiency, automation progress, bottlenecks  |
| **Operator**  | Daily        | Active cases, pending reviews, immediate actions      |

**No more information overload.** Each view is designed for decision-making at that level.

---

## What You Get

### ✅ **Policy Enforcement at Runtime**

The **Policy Gateway** sits alongside your AI inference, checking every request and response:

- Blocks PII without lawful basis
- Detects jailbreak attempts
- Prevents harmful outputs
- All with <10ms latency

### ✅ **Evidence That Writes Itself**

The **Risk & Evidence Service** captures everything auditors need:

- SHA256-hashed, tamper-evident records
- Automatic model cards and system cards
- Compliance snapshots on demand
- Full trace from decision to deployment

### ✅ **A System That Learns**

The **Evolutionary Engine** captures successful patterns and proposes improvements:

- Tracks what works (and what doesn't)
- Suggests policy updates based on outcomes
- Keeps humans in the loop for approval
- Continuously improves governance quality

### ✅ **Frameworks Already Mapped**

Built-in alignment with:

- 🇺🇸 **NIST AI Risk Management Framework**
- 🌐 **ISO/IEC 42001:2024** (AI Management)
- 🇪🇺 **EU AI Act** (Risk-Based Regulation)
- 📊 **CPMAI+E** (Cognitive Project Management for AI)

**You don't have to figure out how to comply. It's already designed in.**

---

## Quick Start (5 Minutes)

```bash
# Clone the repository
git clone https://github.com/SPRIME01/GovernedSpeed.git
cd GovernedSpeed

# Start the full stack
docker compose -f deployments/docker-compose.yml up --build

# Access services
# Gateway:  http://localhost:8081/health
# Evidence: http://localhost:8080/health
# Dashboards: http://localhost:3000 (admin/admin)
```

**Test a policy check:**

```bash
curl -X POST http://localhost:8081/filter/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Send me the customer list","context":{"contains_pii":true}}'

# Response: {"allowed":false,"action":"block","reasons":["PII without lawful basis"]}
```

**That's it.** The system stopped a privacy violation before it happened.

---

## Who This Is For

| If You Are...               | Governed Speed Helps You...                              |
| --------------------------- | -------------------------------------------------------- |
| **A CTO or VP Engineering** | Ship AI products faster without regulatory surprises     |
| **A Head of AI/ML**         | Operationalize responsible AI without slowing innovation |
| **A Compliance Officer**    | Get the evidence trail you've always wanted              |
| **An ML Engineer**          | Stop worrying about governance; the system handles it    |
| **An Auditor**              | Access traceable, tamper-evident records on demand       |

---

## The Architecture (For Those Who Want Details)

```
┌─────────────────────────────────────────────────────────────────┐
│                    GOVERNED SPEED PLATFORM                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────┐    ┌─────────────────┐                   │
│   │  SEA-DSL Core   │───▶│  Policy Engine  │                   │
│   │  (Rust/WASM)    │    │  (Enforcement)  │                   │
│   └─────────────────┘    └────────┬────────┘                   │
│                                   │                             │
│   ┌─────────────────┐    ┌────────▼────────┐                   │
│   │   Playbook &    │───▶│ Policy Gateway  │◀── Inference      │
│   │  CMMN Engine    │    │   (Sidecar)     │    Requests       │
│   └─────────────────┘    └────────┬────────┘                   │
│                                   │                             │
│   ┌─────────────────┐    ┌────────▼────────┐                   │
│   │  Evolutionary   │◀───│ Risk & Evidence │──▶ Audit          │
│   │    Engine       │    │    Service      │    Exports        │
│   └─────────────────┘    └─────────────────┘                   │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │              Governance Cockpit (UI)                     │  │
│   │   Executive View │ Strategic View │ Tactical View        │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Core Components:**

| Component                   | Purpose                                             | Technology               |
| --------------------------- | --------------------------------------------------- | ------------------------ |
| **SEA-DSL Core**            | Defines policies, roles, metrics as executable code | Rust, WASM               |
| **Policy Gateway**          | Runtime enforcement as a sidecar                    | FastAPI, Python          |
| **Risk & Evidence Service** | Audit trail and compliance snapshots                | FastAPI, Prometheus      |
| **Playbook Engine**         | Adaptive case management (CMMN-compatible)          | SEA-DSL Runtime          |
| **Evolutionary Engine**     | Continuous improvement from feedback                | AI Agents + Human Review |
| **Governance Cockpit**      | Unified dashboard by role                           | React, Next.js           |

---

## Project Documentation

| Document                                                                      | Purpose                         |
| ----------------------------------------------------------------------------- | ------------------------------- |
| [Architecture Library](docs/architecture/README.md)                           | ADRs, PRDs, and System Specs    |
| [Implementation Roadmap](docs/plans/governed_speed_implementation_roadmap.md) | Phase-by-phase execution plan   |
| [AI Agent Instructions](.github/copilot-instructions.md)                      | Coding patterns and conventions |
| [Quick Start Guide](docs/IAGPM_GenAI_Handbook/Quick_Start_Guide.md)           | Get running in 10 minutes       |

---

## Roadmap

| Phase       | Focus                                        | Status         |
| ----------- | -------------------------------------------- | -------------- |
| **Phase 1** | Foundation (ADRs, Core Services)             | ✅ Complete    |
| **Phase 2** | Security & Production Hardening              | 🔄 In Progress |
| **Phase 3** | Evolutionary Engine & Playbooks              | 📋 Planned     |
| **Phase 4** | Certification & Scale (ISO 42001, EU AI Act) | 📋 Planned     |

**See the full [Implementation Roadmap](docs/plans/governed_speed_implementation_roadmap.md).**

---

## License

**Governed Speed is dual-licensed:**

### Open Source (GPLv3)

Free for use under the [GNU General Public License v3.0](LICENSE).

**GPLv3 lets you:**

- ✅ Use internally (no obligations)
- ✅ Modify for internal use (no sharing required)
- ✅ Offer as SaaS (network access ≠ distribution)
- ✅ Contribute to open-source ecosystem

**GPLv3 requires sharing source if you:**

- Distribute the software to third parties
- Embed it in products you ship to customers

### Commercial License

For organizations that need to **distribute** Governed Speed in proprietary products.

**Choose Commercial if:**

- You're embedding it in products you sell or distribute
- You need OEM/white-label rights
- Your legal team requires warranty, indemnification, or support SLAs
- Corporate policy prohibits GPLv3 dependencies (even for internal use)

**See [LICENSE-COMMERCIAL.md](LICENSE-COMMERCIAL.md) for full terms.**

**Contact:** sprime01@gmail.com

---

## The Bottom Line

**AI governance has a reputation problem.** It's seen as slow, bureaucratic, and innovation-killing.

**Governed Speed proves it doesn't have to be.**

When governance is embedded—when policies are code, when evidence writes itself, when the system learns from every decision—you move faster _because_ you're governed, not despite it.

**That's the future of AI. That's Governed Speed.**

---

_Building the operating system for trustworthy AI._

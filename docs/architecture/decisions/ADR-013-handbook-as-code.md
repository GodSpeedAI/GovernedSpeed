# ADR-013: Handbook as Code & Operational Source of Truth

**Status:** Accepted  
**Date:** 2025-12-10  
**Deciders:** Architecture Team, Enablement Team  
**Technical Story:** Transition the IAGPM Handbook from a static "Reference Shelf" to a dynamic "Operational Manual" that reflects the living software system.

---

## Context and Problem Statement

The legacy `IAGPM_GenAI_Handbook` described a manual, document-heavy governance process (Word templates, committee meetings, Excel risk registers).
However, the **Governed Speed** platform (Phase 1-3) implements **Automated Governance** (CI/CD gates, RES Evidence Fabric, Playbook Engine).
There is a critical dissonance: The handbook tells users to do things manually that the system automates, and fails to explain how to operate the automated tools.

## Decision Drivers

- **Consistency:** Documentation must match reality.
- **Maintainability:** "Docs as Code" allows us to version the manual alongside the software.
- **User Experience:** Users need to know how to _drive_ the vehicle, not just read about the theory of combustion.

## Decision Outcome

We will refactor the Handbook into **`docs/handbook`** with the following principles:

1.  **Data-Driven Generation**
    - The core "Reference" sections of the Handbook are generated **directly from `sea-dsl` source files**.
    - `Entity`, `Policy`, and `Playbook` definitions include docstrings (`@doc`) that are compiled into MDX.
    - _Old:_ Manually updating a Word doc when a policy changes.
    - _New:_ Changing `policy.sea` automatically updates the "Compliance Manual" site.
2.  **Playbook Centrality:** Strategic process guidance moves to **CMMN Playbooks**. The Handbook explains _how to design_ those Playbooks, not the content of the playbooks themselves (which live in the `playbooks/` repo).
3.  **UI over Meetings:** Replaces descriptions of "Review Meetings" with guides for the **Governance Cockpit** (PRD-010).

## Consequences

### Positive

- **Alignment:** Training materials perfectly match the tools.
- **Agility:** Updates to the code trigger updates to the docs (in the same PR).
- **Scalability:** Users learn to use scalable tools, not unscalable manual processes.

### Negative

- **Effort:** Requires a significant rewrite of existing high-quality text.
- **Transition:** Users familiar with the old manual method (CPMAI standard) may need re-training on the "Automated" version.

## Links

- [docs/plans/handbook_refactor_plan.md](../../plans/handbook_refactor_plan.md)
- [PRD-010: Governance Cockpit](../requirements/PRD-010-governance-cockpit.md)

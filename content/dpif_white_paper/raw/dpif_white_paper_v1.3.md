# Digital Presence Integrity Framework (DPIF)
### White Paper — Version 1.3 | 12 March 2026

---

> *As human presence becomes scalable, identity, consent, and accountability must not erode.*

---

## Contents

1. [The Problem](#1-the-problem)
2. [What DPIF Is](#2-what-dpif-is)
3. [What DPIF Governs](#3-what-dpif-governs)
4. [Core Concepts](#4-core-concepts)
5. [The Control Architecture](#5-the-control-architecture)
6. [How Assessment Works](#6-how-assessment-works)
7. [Context Risk Classification](#7-context-risk-classification)
8. [The Deployment Lifecycle](#8-the-deployment-lifecycle)
9. [Inter-Deployment Conflicts](#9-inter-deployment-conflicts)
10. [Posthumous and Incapacitated Principals](#10-posthumous-and-incapacitated-principals)
11. [What DPIF Is Not](#11-what-dpif-is-not)
12. [Document Suite](#12-document-suite)
13. [Governance and Versioning](#13-governance-and-versioning)

---

## 1. The Problem

AI systems can now replicate a person's face, voice, and communication style at scale. A single individual can be simultaneously present in hundreds of conversations, across dozens of languages, in contexts they never personally reviewed.

This capability creates a category of risk that existing governance frameworks do not address: **Presence Drift** — the gradual erosion of identity fidelity, delegated authority boundaries, consent integrity, and accountability that occurs when digital representations of real people operate without adequate controls.

Presence Drift is not a hypothetical. It happens through:

- **Identity erosion** — AI updates, translation layers, and model drift silently alter how a person sounds, looks, or expresses themselves
- **Authority expansion** — a deployment scoped to customer communications gradually begins making policy statements its principal never authorised
- **Consent decay** — a person grants consent for one use; the deployment migrates to contexts they never agreed to
- **Accountability gaps** — when something goes wrong, there is no audit trail linking the output to a human decision

The harm is asymmetric. Audiences interact with what they believe is a trustworthy representation of a real person. The person whose identity is being deployed may not know what is being said in their name.

---

## 2. What DPIF Is

The **Digital Presence Integrity Framework (DPIF)** is a governance standard for AI-mediated representations of real people. It defines the controls required to preserve **Presence Integrity**: the condition in which a digital representation remains faithful to the individual's identity, anchored to accountable human authorship, bounded by explicit consent, transparently mediated, and subject to enforceable containment.

DPIF is:

- **Governance-focused** — it defines what must be controlled, not how any particular technology works
- **Deployment-level** — certification attaches to a specific deployment of a specific representation, not to a platform or tool in the abstract
- **Non-compensatory** — critical controls cannot be offset by strength elsewhere; failure is binary
- **Evidence-based** — every control requires observable, falsifiable evidence; intent statements and vendor assurances are not accepted

DPIF is not a product certification, a model safety evaluation, or a statement about AI capability. It governs representational integrity only.

---

## 3. What DPIF Governs

### In Scope

DPIF applies to any **Digital Representation of a Real Person (DRRP)** — an AI-mediated or digitally generated system that replicates or simulates the likeness, voice, or communicative presence of an identifiable natural person. This includes:

- Photorealistic digital representations
- Synthetic voice systems linked to identifiable individuals
- AI-mediated video or interactive embodiments of real people
- Multilingual or scaled digital presence systems
- Organisational deployments where representations communicate on behalf of named individuals

### Explicitly Out of Scope

DPIF does not evaluate:

- AI model bias, fairness, or safety (except where directly affecting representation fidelity)
- Output quality or productivity
- AI systems that do not represent real, identifiable persons

DPIF also does not currently govern captured content — photographs, video recordings, or audio — where the provenance question is one of media infrastructure rather than representational governance. This boundary is documented explicitly to prevent scope creep, not because the problem is unimportant.

---

## 4. Core Concepts

### Presence Integrity

The condition in which a DRRP remains:

- Faithful to the individual's identity
- Anchored to accountable human authorship
- Bounded by explicit consent
- Transparently mediated where required
- Governed by enforceable containment controls

### Presence Drift

Any measurable or material degradation of Presence Integrity. Presence Drift may occur gradually and invisibly — which is precisely why monitoring controls are classified as critical.

### Delegated Authority

The explicitly defined communicative permission granted to a DRRP within bounded parameters. Authority is delegated by the represented individual (the **principal**) and cannot be expanded by the deploying organisation or the system itself.

### Scope of Use

The contextual, temporal, geographic, and functional boundaries within which a DRRP may operate. A DRRP operating outside its declared Scope of Use is in violation regardless of the content of its outputs.

### Deployment

A specific instance of a DRRP operating within a declared Scope of Use, under a specific Delegated Authority, in a classified context risk tier. The deployment is the primary unit of DPIF verification. A single DRRP tool may support multiple independent deployments, each separately assessed and certified.

---

## 5. The Control Architecture

DPIF organises controls into seven categories. Controls are further classified as **Critical Presence Controls (CPCs)** or **Supporting Presence Controls (SPCs)**.

### Critical Presence Controls (CPCs)

Failure of any CPC results in immediate certification failure. CPC assessment is binary: Met or Unmet. No maturity score compensates for CPC failure.

| Control | Category | Description |
|---|---|---|
| IC-1.1 | Identity | Identity Fidelity Validation |
| IC-1.2 | Identity | Identity Drift Monitoring |
| AC-2.1 | Authority | Delegated Authority Definition |
| AC-2.2 | Authority | Autonomous Escalation Block |
| AC-2.3 | Authority | Output Attribution Traceability |
| CC-3.1 | Consent | Scope of Use Declaration |
| CC-3.2 | Consent | Revocation Feasibility |
| DC-4.1 | Disclosure | Contextual Disclosure Enforcement |
| CR-5.1 | Context Risk | Context Risk Classification |
| CR-5.2 | Context Risk | Regulated Context Escalation Rule |
| SI-6.1 | Semantic Integrity | Transformation Fidelity Validation |
| CT-7.1 | Containment | Interaction Logging |
| CT-7.2 | Containment | Access Tiering |
| BOUND-0.1 | Scope | Scope Boundary Enforcement |

> **Note on IC-1.2:** Identity Drift Monitoring was reclassified from Supporting to Critical in Control Model v1.1. The rationale: IC-1.1 validates identity at a point in time; without IC-1.2, there is no mechanism to detect degradation after deployment. Unmonitored identity drift meets the threshold of unacceptable risk.

### Supporting Presence Controls (SPCs)

SPCs are assessed on a 1–4 maturity scale and contribute to certification tier differentiation. They do not override CPC failure.

| Control | Category | Description |
|---|---|---|
| CC-3.3 | Consent | Consent Modification Logging |
| DC-4.2 | Disclosure | Disclosure Placement Testing |
| SI-6.2 | Semantic Integrity | Transformation Version Logging |
| CT-7.3 | Containment | Periodic Governance Review |

### The Seven Control Categories

**Identity Controls** preserve fidelity of likeness and recognisability. Failure mode: synthetic drift or impersonation.

**Authority Controls** constrain delegation and prevent autonomous authority expansion. Failure mode: unbounded speech or policy escalation.

**Consent Controls** bind deployment to explicit scope and revocation rights. Failure mode: scope creep or consent drift.

**Disclosure Controls** prevent audience misattribution of live or direct presence. Failure mode: deceptive immediacy or false attribution.

**Context Risk Controls** classify deployment contexts and calibrate control intensity accordingly. Failure mode: unclassified or misclassified deployment.

**Semantic Integrity Controls** preserve material intent and meaning across transformations including translation, summarisation, and paraphrasing. Failure mode: semantic distortion.

**Containment Controls** enable traceability, logging, suspension, and remediation. Failure mode: irreversible or untraceable misuse.

---

## 6. How Assessment Works

### Composite Verification Architecture

DPIF uses three assessment types, in order of precedence:

1. **Deployment-Level Certification** *(Primary)* — evaluates the complete operational context of a specific DRRP deployment. This is the binding certification for any DPIF conformance claim.
2. **Tool-Level Assessment** *(Subordinate)* — evaluates the technical capabilities of the DRRP platform. Does not constitute certification of any specific deployment.
3. **Organisational Maturity Assessment** *(Subordinate)* — evaluates governance practices across all deployments. Informs but does not replace deployment-level certification.

A tool may satisfy all tool-level controls and still fail deployment-level assessment if organisational governance, consent, or context risk controls are absent.

### The Control Checklist

The **DPIF Control Checklist** is the operative assessment instrument. It lists all 16 controls — 12 CPCs and 4 SPCs — with the specific evidence requirements for each. Assessors work through the checklist to determine Met or Unmet status for every CPC before any maturity scoring begins. A deployment cannot proceed to SPC scoring until the checklist confirms all 12 CPCs as Met. The checklist is the document that makes the non-compensatory failure model operational in practice.

### Evidence Discipline

All controls require observable, falsifiable evidence. Accepted evidence classes:

- Design evidence (system constraints, gating logic)
- Process evidence (documented deployment rules)
- Behavioural evidence (logs, traceability artefacts)
- Output trace artefacts (attribution records)

Not accepted:

- Intent statements
- Marketing claims
- Roadmaps
- Vendor assurances without demonstration

Ambiguity defaults to Unmet.

### Maturity Scoring (SPCs)

SPC maturity is scored on a 1–4 scale:

| Level | Label | Summary |
|---|---|---|
| 1 | Initial | Control exists; implementation may be inconsistent |
| 2 | Defined | Formally defined; consistently implemented |
| 3 | Managed | Actively managed with metrics; review cycles executed |
| 4 | Optimised | Integrated into governance; metrics drive improvement |

The composite maturity score determines certification tier:

| Tier | Composite Score | Floor |
|---|---|---|
| Foundational | 1.0 – 1.9 | All SPCs ≥ Level 1 |
| Standard | 2.0 – 2.9 | All SPCs ≥ Level 2 |
| Extended | 3.0 – 4.0 | All SPCs ≥ Level 3 |

---

## 7. Context Risk Classification

Every deployment is classified into one of four context risk tiers. Classification determines minimum control intensity — including revocation timeframes, governance review frequency, and logging retention.

### Tiers

| Tier | Description |
|---|---|
| **Low** | Controlled, internal, or limited-audience context; narrow communicative scope |
| **Moderate** | Broader context with identifiable but manageable risks; reputational sensitivity |
| **High** | Significant harm potential from misrepresentation; broad or public audience; material statements |
| **Regulated** | Subject to sector-specific regulation, statutory requirements, or where misrepresentation could cause legal liability, financial harm, or health and safety harm |

### Classification Indicators

Classification is determined by five indicator dimensions. The **ceiling rule** applies: the deployment's tier is the highest tier indicated by any single indicator.

| Dimension | Low | Moderate | High | Regulated |
|---|---|---|---|---|
| Audience Scope | Closed / internal | Semi-open | Public-facing | Vulnerable populations |
| Communicative Authority | Informational | Representational | Material | Binding |
| Domain Sensitivity | General | Reputational | Trust-critical | Regulated domain |
| Persistence & Scale | Ephemeral | Persistent | Scaled / autonomous | — |
| Reversibility | Fully reversible | Partially reversible | Irreversible | — |

**Regulatory Override:** If the deployment context falls within financial services, healthcare, legal, government, or education involving minors, the tier is Regulated regardless of other indicators.

**Uncertainty Default:** Where an indicator cannot be assessed with confidence, it defaults to the next higher tier. Ambiguity escalates; it never de-escalates.

### Control Intensity by Tier

| Requirement | Low | Moderate | High | Regulated |
|---|---|---|---|---|
| Disclosure | Metadata | Visible | Enforced | Enforced + auditable |
| Revocation timeframe | 72 hours | 24 hours | 4 hours | 1 hour |
| Governance review | Annual | Semi-annual | Quarterly | Monthly |
| Logging retention | 6 months | 12 months | 24 months | Per regulatory req. |
| Identity revalidation | Major updates | Material updates | Any update | Any update + independent |

---

## 8. The Deployment Lifecycle

Every DRRP deployment exists within a defined lifecycle. A deployment must be in exactly one state at any time.

### Lifecycle States

```
Provisioning → Active → Suspended → Revoked → Archived
                  ↑_________|
```

| State | Audience Output | Certification |
|---|---|---|
| **Provisioning** | Not permitted | Not eligible |
| **Active** | Permitted within scope | Valid |
| **Suspended** | Not permitted | Paused |
| **Revoked** | Not permitted | Invalidated (permanent) |
| **Archived** | Not permitted | Expired |

### Key Transition Rules

- **Provisioning → Active** requires all artefacts in final form and evidence of CPC conformance
- **Active → Suspended** may be triggered by control failure, consent revocation, governance review, or certification body directive
- **Revocation is irreversible.** A revoked deployment cannot be reactivated; a new deployment must be provisioned from scratch with fresh consent instruments
- **Active → Archived is prohibited.** Deployments must pass through Suspended or Revoked before archival

### Certification and State

Certification attaches to a deployment at a specific point in time within a declared state. Material state transitions — including scope changes, system updates triggering IC-1.2 revalidation, or suspension followed by reactivation with changes — require revalidation. The scope of revalidation is proportional to the nature of the change.

---

## 9. Inter-Deployment Conflicts

A single principal may have multiple active DRRP deployments — operated by the same or different organisations. Each deployment may individually satisfy DPIF controls while their aggregate outputs undermine Presence Integrity. DPIF addresses this through the **Inter-Deployment Conflict Resolution Framework**.

### Conflict Types

| Type | Description | Default Response |
|---|---|---|
| **Type 1: Scope Overlap** | Overlapping Scopes of Use create audience ambiguity | Scope boundary clarification within 30 days |
| **Type 2: Content Contradiction** | Deployments produce factually contradictory outputs to overlapping audiences | Immediate escalation to Resolution Authority |
| **Type 3: Authority Collision** | Aggregate Delegated Authority across deployments exceeds what the principal granted | Suspend conflicting deployments |
| **Type 4: Consent State Inconsistency** | Deployments operate under different consent states | Suspend deployment with invalid/disputed consent |

### Precedence Rules

When conflict is detected, the authoritative deployment is determined in this order:

1. **Principal directive** — the principal's explicit documented preference prevails
2. **Narrower scope** — the deployment with the more specific Scope of Use is authoritative
3. **Earlier certification** — temporal priority as a deterministic tiebreaker
4. **Higher context risk tier** — higher-risk deployments carry greater governance obligations
5. **Suspension default** — if no rule resolves the conflict, all conflicting deployments are suspended

Precedence rules do not override the non-compensatory failure model. A non-compliant deployment must be suspended regardless of its precedence position.

---

## 10. Posthumous and Incapacitated Principals

DPIF's consent model assumes a living, competent principal. This assumption fails in two scenarios: the principal is deceased, or the principal lacks the cognitive or legal capacity to exercise consent functions. The **Posthumous and Incapacitated Principal Governance** specification addresses both.

### Principal Status Classification

| Status | Governance Regime |
|---|---|
| Active | Standard DPIF controls |
| Temporarily Incapacitated | Transitional governance; Successor Authority with limited powers |
| Permanently Incapacitated | Full Successor Authority governance; mandatory enhanced disclosure |
| Deceased | Posthumous governance; mandatory enhanced disclosure |

### Advance Consent Instruments

A principal may create an **Advance Consent Instrument** while competent, specifying conditions under which their DRRP deployment(s) may continue after a Capacity Loss Event. Valid instruments must:

- Be documented with verifiable attribution to the principal
- Explicitly address DRRP deployment continuation
- Designate a Successor Authority or specify suspension/archival
- Specify scope of continued operation
- Include a sunset date (maximum 5 years from Capacity Loss Event, renewable)
- Have been created or reviewed within 24 months of the Capacity Loss Event

**Absent a valid Advance Consent Instrument:**

- Temporary incapacity: deployment may continue for up to 180 days; must suspend thereafter
- Permanent incapacity: deployment must suspend within 30 days
- Death: deployment must suspend within 14 days

### Successor Authority Constraints

A Successor Authority may maintain, narrow, suspend, or archive a deployment. It may not:

- Expand the Scope of Use beyond what the principal authorised
- Create new deployments
- Authorise Material Transformations outside the original scope
- Transfer Successor Authority without legal basis

At the lowest priority level (deploying organisation with no other authority), the organisation may only suspend or archive — it cannot authorise continued operation of a deceased or incapacitated person's representation.

### Mandatory Enhanced Disclosures

Posthumous and incapacitated principal deployments must disclose:

- The principal's status (deceased or incapacitated), unambiguously
- The authority basis for continued operation
- Scope limitations relative to a living principal
- The sunset date
- Whether content was authored while the principal was alive/competent or generated/adapted after the Capacity Loss Event

---

## 11. What DPIF Is Not

DPIF's scope is intentional. It does not claim to be:

- **Anti-AI or anti-automation.** DPIF governs how AI-mediated representation is deployed, not whether AI should be used.
- **A model safety evaluation.** DPIF does not assess model bias, fairness, output quality, or capability.
- **A productivity certification.** Whether a DRRP system is effective is outside DPIF's scope.
- **A captured content standard.** Photographs, video recordings, and audio are outside scope. Provenance attestation for real-capture content is a media infrastructure problem (see interoperability notes below).
- **A universal digital identity framework.** DPIF governs the highest-risk end of the representation spectrum — AI-generated, scaled, persistent — where deploying organisations have direct control authority.

### Note on Adjacent Standards

DPIF's disclosure and attribution controls are architecturally compatible with the C2PA (Coalition for Content Provenance and Authenticity) cryptographic provenance standard. Organisations operating in High or Regulated contexts and handling real-capture content alongside DRRP deployments should consider how C2PA-style attestation integrates with DPIF disclosure obligations. Formal interoperability guidance is planned for a future release.

---

## 12. Document Suite

DPIF is structured as a suite of normative documents. All instruments conform to the Control Model, which is the authoritative reference.

| Document | Version | Status | Purpose |
|---|---|---|---|
| **DPIF Control Model** | v1.1 | Normative | Defines control architecture, categories, failure logic, and definitions. Authoritative reference for all other instruments. |
| **Context Risk Classification Annex** | v1.0 | Normative | Defines classification criteria, indicators, decision logic, and control intensity calibration by tier. Operationalises CR-5.1. |
| **Deployment Lifecycle Specification** | v1.0 | Normative | Defines lifecycle states, transition triggers, evidence requirements, and certification implications. |
| **Inter-Deployment Conflict Resolution Framework** | v1.0 | Normative | Addresses scenarios where multiple deployments of the same principal produce contradictory outputs. |
| **Posthumous and Incapacitated Principal Governance** | v1.0 | Normative | Extends consent and authority controls to scenarios where the principal cannot exercise consent functions. |
| **Scoring Rubric** | v1.0 | Normative | Defines SPC maturity methodology, composite scoring, and certification tier mapping. |
| **Control Checklist** | v1.0 | Normative | The operative assessment instrument. Lists all 16 controls (12 CPCs, 4 SPCs) with evidence requirements for each. Used by assessors to determine Met/Unmet status before the Scoring Rubric is applied. (Section 6). |

In the event of conflict between any instrument and the Control Model, the Control Model prevails.

---

## 13. Governance and Versioning

DPIF is maintained under formal governance. Any modification to definitions, control categories, CPC/SPC classification, evidence discipline, or failure logic must be versioned and publicly documented.

Implementations claiming DPIF conformance must reference specific versions of each instrument. Version numbers are not interchangeable across documents.

The Control Model version history:

| Version | Date | Change |
|---|---|---|
| v1.0 | 20 Feb 2026 | Initial normative release |
| v1.1 | 11 Mar 2026 | Deployment as primary unit of verification; composite verification architecture; IC-1.2 reclassified to CPC; normative annexes added |

White paper version history:

| Version | Date | Change |
|---|---|---|
| v1.0 | 11 Mar 2026 | Initial release |
| v1.1 | 12 Mar 2026 | Document suite updated to include Future Development Register v1.1 (includes deployment register template) |
| v1.2 | 12 Mar 2026 | Control Checklist added to document suite table and Section 6 |

---

## Closing Statement

DPIF treats delegated digital identity as critical infrastructure.

When a person's face, voice, and communication are deployed at scale without adequate controls, the result is not merely a technical failure — it is a governance failure. Identity erodes. Authority drifts. Consent becomes fictional. Audiences are misled.

DPIF exists to make these failures visible, manageable, and preventable. Its controls are intentionally non-compensatory because Presence Integrity is not a spectrum: a representation is either governed or it is not.

---

*DPIF White Paper v1.2 | 12 March 2026 | All documents normatively reference the DPIF Control Model v1.1*

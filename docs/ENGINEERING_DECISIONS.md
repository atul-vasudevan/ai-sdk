# Engineering Decisions

This document outlines the key engineering decisions made in this repository, the rationale behind them, and the trade-offs involved.  
The goal is to demonstrate **production-minded AI system design**, not just feature delivery.

---

## 1. Shared Internal AI SDK (`ai_lib`)

### Decision
Introduce a shared internal Python SDK (`ai_lib`) instead of letting services call models directly.

### Why
- Centralises AI logic (models, prompts, tracing, configuration)
- Prevents duplication across services
- Enables consistent observability, evaluation, and guardrails
- Makes it easier to evolve AI behaviour without touching every service

### Trade-offs
- Adds an abstraction layer
- Requires versioning discipline

### Rationale
This mirrors how AI is typically scaled across teams: a **platform layer** that enables product teams to consume AI safely and consistently.

---

## 2. Deterministic Defaults for CI and Evaluation

### Decision
Default model execution to **deterministic decoding** for tests and CI.

### Why
- Ensures reproducible outputs
- Makes golden dataset evaluation reliable
- Prevents flaky CI failures

### Trade-offs
- Deterministic decoding may reduce perceived output quality compared to sampling

### Rationale
Reliability and regression detection are higher priority than stylistic variation in automated quality gates.  
Sampling can be enabled later in production behind configuration flags.

---

## 3. Golden Dataset Evaluation

### Decision
Use golden datasets to validate model behaviour instead of relying on manual review or ad-hoc testing.

### Why
- AI output changes over time (model updates, prompt changes, config tweaks)
- Golden datasets act as **behavioural contracts**
- Prevent silent regressions

### Trade-offs
- Golden datasets require maintenance
- Changes must be reviewed deliberately

### Rationale
Golden datasets provide a scalable alternative to a QA team and enable teams to reason about AI quality changes explicitly.

---

## 4. Simple Guardrails at the Service Boundary (Guardrails v1)

### Decision
Implement minimal runtime guardrails at the API boundary:
- Input validation (non-empty, max length)
- Optional API key authentication
- Output sanity check (summary must be shorter than input)

### Why
- Prevents obvious abuse and cost blowups
- Ensures the system fails fast on invalid requests
- Establishes a clear security and responsibility boundary

### Trade-offs
- Does not cover advanced risks (PII detection, moderation, rate limiting)
- Guardrails are intentionally conservative

### Rationale
This repository demonstrates the **pattern**, not exhaustive enforcement.  
In production, these guardrails would be extended incrementally as risk increases.

---

## 5. Optional API Key Authentication

### Decision
Support optional API-key-based authentication using `X-API-Key` and an environment variable.

### Why
- Keeps local development frictionless
- Enables basic security in shared or production environments
- Makes the service boundary explicit

### Trade-offs
- Not a full auth solution (no OAuth/JWT)

### Rationale
This is a pragmatic starting point. In real deployments, authentication would typically be handled by an API gateway or identity provider.

---

## 6. Observability via Langfuse

### Decision
Integrate Langfuse for tracing AI operations.

### Why
- Enables visibility into inputs, outputs, and errors
- Critical for debugging AI systems in production
- Allows future evaluation and drift analysis

### Trade-offs
- Requires external service configuration
- Adds small runtime overhead

### Rationale
AI systems are non-deterministic and opaque by default. Observability is essential, not optional.

---

## 7. Separation of Concerns: Service vs Infrastructure

### Decision
Keep application logic, containerisation, orchestration, and infrastructure definitions separate:
- Application code in `ai_lib/` and `service/`
- Docker for packaging
- Kubernetes manifests for orchestration
- Terraform for infrastructure provisioning

### Why
- Aligns with real-world deployment practices
- Enables GitOps workflows (e.g. Argo CD)
- Keeps responsibilities clear and auditable

### Trade-offs
- More files and folders
- Slightly higher cognitive load for newcomers

### Rationale
This separation reflects how production systems are built and operated, even if not all components are exercised locally.

---

## 8. Makefile as Developer Interface

### Decision
Use a Makefile to standardise common workflows.

### Why
- Provides a single, discoverable entry point
- Reduces cognitive load for contributors
- Encodes “how the system is meant to be used”

### Trade-offs
- Adds another abstraction layer

### Rationale
A Makefile acts as executable documentation and is especially valuable when multiple tools (CI, Docker, K8s, Terraform) are involved.

---

## 9. Incremental Scope by Design

### Decision
Deliberately keep some aspects minimal or stubbed:
- No advanced moderation
- No rate limiting
- No full auth stack
- No model retraining pipelines

### Why
- Focus on **foundational correctness**
- Avoid overengineering
- Keep the repository understandable and reviewable

### Rationale
The goal is to demonstrate **engineering judgement and patterns**, not to simulate a full enterprise platform.

---

It is designed to show how AI systems can be built in a way that is **scalable, testable, and trustworthy**, even with simple models and limited infrastructure.
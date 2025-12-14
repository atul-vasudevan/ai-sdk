# 📦 AI SDK + Microservice

> **A minimal, production-minded AI platform demonstrating an internal Python SDK, observability, evaluation, containerisation, and deployment scaffolding.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)
![Langfuse](https://img.shields.io/badge/Observability-Langfuse-red)

---

## 🔍 Overview

This repository contains two core components designed to simulate a scalable internal AI platform:

### **1. `ai_lib/` — Internal Python AI SDK**
A modular Python library that serves as the foundation for AI capabilities across the organization. It provides:
- 🛠 A unified `AIClient` interface
- 📝 Text summarisation capability (`simple` and HuggingFace backends)
- 🔭 Built-in observability via **Langfuse**
- ⚙️ Clean configuration patterns
- 🧰 Reusable utilities for downstream services

### **2. `service/` — Example FastAPI Microservice**
A lightweight microservice that consumes the SDK to expose AI capabilities via REST API:
- `GET /health` — Health check
- `POST /summarise` — Text summarisation endpoint

---

## 🧱 Architecture

This structure demonstrates **Shared SDK → Multiple Services**, **Testing + LLM Evaluation**, and **GitOps-ready packaging**.

```plaintext
ai-sdk/
│
├── ai_lib/                 ← Internal SDK (core library)
│   ├── client.py
│   ├── summarisation/
│   ├── tracing/
│   ├── tests/
│   └── ...
│
├── service/                ← FastAPI microservice using lib
│   ├── app/               ← Service code
│   ├── k8s/               ← Kubernetes manifests
│   └── DockerFile         ← Container definition
├── terraform/              ← Infrastructure as Code
├── eval/                   ← DeepEval test suite
├── pyproject.toml
└── README.md
```

---

## 🧩 Features

### Internal AI SDK (`ai_lib`)
- **Unified API:** `AIClient.summarise_text()` abstraction.
- **Backend Agnostic:** Select backends via env vars (`simple`, `hf`).
- **Observability:** Built-in Langfuse tracing via `traced_operation()`.
- **Extensible:** Designed for clean architectural extension.

### Microservice
- **FastAPI Integration:** Shows how downstream teams consume the SDK.
- **Production Ready:** Deployable via Docker or Kubernetes.

### Quality & Governance
- **Unit Tests:** Located in `tests/`.
- **LLM Evals:** DeepEval test suite in `eval/`.
- **CI/CD:** GitHub Actions pipeline included.

### Infrastructure Scaffolding
- **Containerisation:** Dockerfile included.
- **Orchestration:** Kubernetes Deployment + Service manifests.
- **IaC:** Terraform stub for namespace provisioning.
- **GitOps:** Structure ready for Argo CD.

---

## 🚀 Running Locally

### 1. Install the SDK (Development Mode)
```bash
pip install -e ".[dev]"
```

### 2. Run the Microservice
```bash
pip install -r service/requirements.txt
uvicorn service.app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Test Endpoints

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Summarise Text:**
```bash
curl -X POST http://localhost:8000/summarise \
  -H "Content-Type: application/json" \
  -d '{"text": "Bella is a 3-year-old indoor cat..."}'
```

---

## 🐳 Running via Docker

**Build the image:**
```bash
docker build -f service/DockerFile -t ai-summarise-service .
```

**Run the container:**
```bash
docker run -p 8000:8000 \
  -e AI_LIB_SUMMARISATION_BACKEND=simple \
  ai-summarise-service
```

---

## 👀 Observability with Langfuse

To enable tracing, set the following environment variables:

```bash
export LANGFUSE_SECRET_KEY=...
export LANGFUSE_PUBLIC_KEY=...
export LANGFUSE_HOST=[https://cloud.langfuse.com](https://cloud.langfuse.com)
```

Any SDK call wrapped with the tracer will appear in your Langfuse dashboard:

```python
with traced_operation("summarise_text", inputs={"text": text}):
    # ... logic
```

---

## 🧪 Testing & Evaluation

**Unit Tests:**
```bash
pytest tests
```

**DeepEval Tests:**
```bash
pytest eval
```

> Both test suites run automatically in the GitHub Actions pipeline.

---

## 🔄 CI/CD & Deployment

### CI Pipeline (GitHub Actions)
The pipeline replicates how production AI teams enforce quality:
1. Installs dependencies.
2. Runs unit tests.
3. Runs DeepEval tests (supports Langfuse-enabled evals).

### ☸️ Kubernetes Deployment

**Prerequisites:**
- Minikube installed and running
- kubectl configured

**Quick Start:**
```bash
# 1. Create namespace with Terraform
cd terraform && terraform apply

# 2. Build image in Minikube's Docker
eval $(minikube docker-env)
docker build -f service/DockerFile -t ai-summarise-service:latest .

# 3. Create secrets (if using Langfuse)
kubectl create secret generic langfuse-secrets \
  --from-literal=secret-key='your-key' \
  --from-literal=public-key='your-key' \
  -n ai-platform

# 4. Deploy to Kubernetes
kubectl apply -f service/k8s/deployment.yml
kubectl apply -f service/k8s/service.yml

# 5. Access the service
kubectl port-forward service/ai-summarise-service 8000:80 -n ai-platform
```

### 🔨 Terraform Setup
Infrastructure as Code (IaC) for managing Kubernetes infrastructure.

**Quick Start:**
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

Creates the `ai-platform` namespace.

---

## 🎯 Why This Project Exists

This repository demonstrates the **full lifecycle of AI platform engineering**:

* Shared internal SDK
* Evaluation & Observability
* Microservice Integration
* Docker Containerisation
* CI/CD Automation
* Infra + GitOps Deployment Patterns

It is intended as a hands-on, end-to-end example of what a modern AI platform looks like.

---

## 📚 Future Enhancements

- [ ] Publish `ai_lib` to a private PyPI registry.
- [ ] Add Argo CD Application manifest.
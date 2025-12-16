# Deployment Guide

## Prerequisites
- Docker installed
- Kubernetes cluster (local with minikube/kind, or cloud: GKE, EKS, AKS)
- kubectl configured to access your cluster
- Docker registry account (Docker Hub, GCR, ECR, etc.)

## Deployment Order

### Step 1: Build the Docker Image

```bash
# From the project root
docker build -f service/DockerFile -t your-docker-user/ai-summarise-service:latest .
```

Replace `your-docker-user` with your Docker Hub username or registry path.

### Step 2: Push Image to Registry

```bash
# Login to your registry (if needed)
docker login

# Push the image
docker push your-docker-user/ai-summarise-service:latest
```

**Alternative registries:**
- **Google Container Registry (GCR):** `gcr.io/your-project/ai-summarise-service:latest`
- **AWS ECR:** `your-account.dkr.ecr.region.amazonaws.com/ai-summarise-service:latest`
- **Azure ACR:** `your-registry.azurecr.io/ai-summarise-service:latest`

### Step 3: Update Deployment YAML

Edit `service/k8s/deployment.yml` and replace:
```yaml
image: your-docker-user/ai-summarise-service:latest
```
with your actual image path.

### Step 4: Create Secrets (Optional - only if using Langfuse)

**Option A: Using kubectl (quick)**
```bash
kubectl create secret generic langfuse-secrets \
  --from-literal=secret-key='sk-lf-xxxxx' \
  --from-literal=public-key='pk-lf-xxxxx'
```

**Option B: Using YAML file (recommended for version control)**
```bash
# Copy the example
cp service/k8s/secrets.yml.example service/k8s/secrets.yml

# Edit secrets.yml with your actual values
# Then apply
kubectl apply -f service/k8s/secrets.yml
```

**Option C: Using CI/CD**
- Store secrets in your CI/CD system's secret manager
- Have your pipeline create the secret before deployment

### Step 5: Uncomment Secrets in Deployment (if using Langfuse)

Edit `service/k8s/deployment.yml` and uncomment the Langfuse secret references:
```yaml
- name: LANGFUSE_SECRET_KEY
  valueFrom:
    secretKeyRef:
      name: langfuse-secrets
      key: secret-key
- name: LANGFUSE_PUBLIC_KEY
  valueFrom:
    secretKeyRef:
      name: langfuse-secrets
      key: public-key
- name: LANGFUSE_HOST
  value: "https://cloud.langfuse.com"
```

### Step 6: Deploy to Kubernetes

```bash
# Apply the deployment
kubectl apply -f service/k8s/deployment.yml

# Apply the service
kubectl apply -f service/k8s/service.yml
```

### Step 7: Verify Deployment

```bash
# Check if pods are running
kubectl get pods -l app=ai-summarise-service

# Check deployment status
kubectl get deployment ai-summarise-service

# Check service
kubectl get service ai-summarise-service

# View logs
kubectl logs -l app=ai-summarise-service

# Test the service (if you have port-forwarding or ingress)
kubectl port-forward service/ai-summarise-service 8000:80
# Then test: curl http://localhost:8000/health
```

## Quick Start (Local Testing with Minikube)

```bash
# Start minikube
minikube start

# Build image in minikube's Docker daemon
eval $(minikube docker-env)
docker build -f service/DockerFile -t ai-summarise-service:latest .

# Update deployment.yml to use: image: ai-summarise-service:latest

# Deploy
kubectl apply -f service/k8s/deployment.yml
kubectl apply -f service/k8s/service.yml

# Access the service
minikube service ai-summarise-service
```

## Troubleshooting

```bash
# Check pod status
kubectl describe pod -l app=ai-summarise-service

# View pod logs
kubectl logs <pod-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Delete and redeploy
kubectl delete -f service/k8s/deployment.yml
kubectl apply -f service/k8s/deployment.yml
```


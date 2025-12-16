# Terraform Infrastructure as Code

This directory contains Terraform configuration for provisioning Kubernetes infrastructure.

## What is Terraform?

**Terraform is Infrastructure as Code (IaC)** - it lets you define and manage infrastructure using code instead of clicking through UIs.

### Benefits:
- **Version Control:** Infrastructure changes are tracked in git
- **Reproducibility:** Same code = same infrastructure every time
- **Collaboration:** Team members can review and approve infrastructure changes
- **Automation:** Can be integrated into CI/CD pipelines

## What This Does

This Terraform configuration creates:
- **Kubernetes Namespace:** `ai-platform` for your AI services

## Prerequisites

1. **Install Terraform:**
   ```bash
   # macOS
   brew install terraform
   
   # Or download from: https://www.terraform.io/downloads
   ```

2. **Configure kubectl:**
   ```bash
   # Make sure kubectl is configured and pointing to your cluster
   kubectl get nodes
   ```

3. **Install Kubernetes provider:**
   ```bash
   terraform init
   ```
   This downloads the Kubernetes provider plugin.

## Usage

### 1. Initialize Terraform
```bash
cd terraform
terraform init
```

This downloads the required providers and sets up Terraform.

### 2. Review What Will Be Created
```bash
terraform plan
```

This shows you what resources Terraform will create/modify/destroy without actually making changes.

### 3. Apply the Configuration
```bash
terraform apply
```

This creates the namespace in your Kubernetes cluster.

**You'll be prompted to confirm.** Type `yes` to proceed.

### 4. Verify
```bash
# Check that the namespace was created
kubectl get namespace ai-platform

# Or see all namespaces
kubectl get namespaces
```

### 5. Destroy (Optional)
If you want to remove the infrastructure:
```bash
terraform destroy
```

## File Structure

```
terraform/
├── main.tf          # Main Terraform configuration
├── .gitignore      # Ignores state files and secrets
└── README.md       # This file
```

## How It Works

1. **Terraform reads** `main.tf`
2. **Connects to Kubernetes** using your kubeconfig
3. **Plans changes** - shows what will be created
4. **Applies changes** - creates the namespace
5. **Stores state** - remembers what it created (in `terraform.tfstate`)

## State Management

Terraform stores state in `terraform.tfstate` (local file by default).

## Common Commands

```bash
# Initialize
terraform init

# Plan (preview changes)
terraform plan

# Apply (create resources)
terraform apply

# Show current state
terraform show

# List resources
terraform state list

# Destroy everything
terraform destroy

# Format code
terraform fmt

# Validate configuration
terraform validate
```

## Integration with Kubernetes Deployment

After creating the namespace with Terraform:

1. **Deploy your application:**
   ```bash
   # Update deployment.yml to use the namespace
   # Add: namespace: ai-platform
   
   kubectl apply -f service/k8s/deployment.yml -n ai-platform
   kubectl apply -f service/k8s/service.yml -n ai-platform
   ```

2. **Or update deployment.yml:**
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: ai-summarise-service
     namespace: ai-platform  # Add this
   # ... rest of config
   ```

## Troubleshooting

### Error: "Kubernetes cluster unreachable"
- Make sure kubectl is configured: `kubectl get nodes`
- Check your kubeconfig: `kubectl config view`

### Error: "Namespace already exists"
- Either delete it: `kubectl delete namespace ai-platform`
- Or import it: `terraform import kubernetes_namespace_v1.ai_platform ai-platform`

### State file issues
- If state gets out of sync, you can refresh: `terraform refresh`
- Or re-import resources: `terraform import`
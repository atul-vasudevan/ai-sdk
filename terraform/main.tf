terraform {
  required_version = ">= 1.0"
}

provider "kubernetes" {
  config_path = "~/.kube/config"
  config_context = "minikube"
}

resource "kubernetes_namespace_v1" "ai_platform" {
  metadata {
    name = "ai-platform"
    
    labels = {
      app     = "ai-platform"
      managed = "terraform"
    }
    
    annotations = {
      description = "Namespace for AI SDK services and applications"
    }
  }
}

output "namespace_name" {
  description = "Name of the created namespace"
  value       = kubernetes_namespace_v1.ai_platform.metadata[0].name
}

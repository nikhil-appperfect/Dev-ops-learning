output "namespace" {
  description = "The Kubernetes namespace created for the chat application"
  value       = kubernetes_namespace.chat_app.metadata[0].name
}

output "frontend_service" {
  description = "The frontend service name"
  value       = module.frontend.service_name
}

output "backend_service" {
  description = "The backend service name"
  value       = module.backend.service_name
}

output "mongodb_service" {
  description = "The MongoDB service name"
  value       = module.mongodb.service_name
}

output "ingress_enabled" {
  description = "Whether ingress is enabled"
  value       = var.ingress.enabled
}

output "ingress_namespace" {
  description = "The namespace where the ingress controller is deployed"
  value       = var.ingress.enabled ? "ingress-nginx" : null
}

output "ingress_url" {
  description = "The full URL to access the application via ingress (when enabled)"
  value       = var.ingress.enabled ? "http://localhost:8080" : null
}

output "ingress_frontend_path" {
  description = "The path configured for the frontend service in the ingress"
  value       = var.ingress.enabled ? "/" : null
}

output "ingress_backend_path" {
  description = "The path configured for the backend service in the ingress"
  value       = var.ingress.enabled ? "/api" : null
}

output "access_instructions" {
  description = "Instructions to access the application"
  value       = var.ingress.enabled ? local.ingress_access_instructions : local.port_forward_access_instructions
}

locals {
  port_forward_access_instructions = <<-EOT
    To access the chat application:

    1. Run the following commands in separate terminals:
       kubectl port-forward svc/${module.frontend.service_name} ${module.frontend.service_port}:${module.frontend.service_port} --address=0.0.0.0 -n ${kubernetes_namespace.chat_app.metadata[0].name}
       kubectl port-forward svc/${module.backend.service_name} ${module.backend.service_port}:${module.backend.service_port} --address=0.0.0.0 -n ${kubernetes_namespace.chat_app.metadata[0].name}

    2. Open your browser and navigate to http://localhost:${module.frontend.service_port}
  EOT

  ingress_access_instructions = <<-EOT
    To access the chat application using Ingress:

    1. Run the following command to enable port forwarding for the Ingress controller:
       kubectl port-forward -n ingress-nginx service/ingress-nginx-controller 8080:80 --address=0.0.0.0

    2. Open your browser and navigate to http://localhost:8080
       - Frontend is available at http://localhost:8080
       - Backend API is available at http://localhost:8080/api
  EOT
}
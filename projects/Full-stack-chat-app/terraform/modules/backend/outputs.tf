output "service_name" {
  description = "The name of the backend service"
  value       = kubernetes_service.backend.metadata[0].name
}

output "service_port" {
  description = "The port of the backend service"
  value       = kubernetes_service.backend.spec[0].port[0].port
}

output "deployment_name" {
  description = "The name of the backend deployment"
  value       = kubernetes_deployment.backend.metadata[0].name
}
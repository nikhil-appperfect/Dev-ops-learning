output "service_name" {
  description = "The name of the frontend service"
  value       = kubernetes_service.frontend.metadata[0].name
}

output "service_port" {
  description = "The port of the frontend service"
  value       = kubernetes_service.frontend.spec[0].port[0].port
}

output "deployment_name" {
  description = "The name of the frontend deployment"
  value       = kubernetes_deployment.frontend.metadata[0].name
}
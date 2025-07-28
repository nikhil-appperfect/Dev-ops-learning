output "ingress_name" {
  description = "The name of the ingress resource"
  value       = kubernetes_ingress_v1.chat_app_ingress.metadata[0].name
}


output "ingress_host" {
  description = "The hostname for the ingress"
  value       = var.ingress_host
}


output "ingress_namespace" {
  description = "The namespace of the ingress resource"
  value       = kubernetes_ingress_v1.chat_app_ingress.metadata[0].namespace
}


output "creation_timestamp" {
  description = "The timestamp when the ingress resource was created"
  value       = kubernetes_ingress_v1.chat_app_ingress.metadata[0].generation
}


output "frontend_path" {
  description = "The path configured for the frontend service"
  value       = "/"
}


output "backend_path" {
  description = "The path configured for the backend service"
  value       = "/api"
}


output "ingress_url" {
  description = "The full URL to access the application via ingress"
  value       = "http://localhost:8080"
}
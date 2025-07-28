output "namespace" {
  description = "The Kubernetes namespace created for the Notes App"
  value       = kubernetes_namespace.notes_app.metadata[0].name
}

output "notes_app_service_name" {
  description = "The name of the Notes App service"
  value       = kubernetes_service.notes_app.metadata[0].name
}

output "nginx_service_name" {
  description = "The name of the Nginx service"
  value       = kubernetes_service.nginx.metadata[0].name
}

output "ingress_name" {
  description = "The name of the Ingress resource"
  value       = kubernetes_ingress_v1.notes_app_ingress.metadata[0].name
}

output "access_instructions" {
  description = "Instructions to access the application"
  value       = "Run: kubectl port-forward svc/ingress-nginx-controller 8080:80 -n ingress-nginx --address=0.0.0.0"
}
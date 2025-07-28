output "service_name" {
  description = "The name of the MongoDB service"
  value       = kubernetes_service.mongo.metadata[0].name
}

output "pvc_name" {
  description = "The name of the MongoDB PVC"
  value       = kubernetes_persistent_volume_claim.mongodb_pvc.metadata[0].name
}

output "connection_string" {
  description = "MongoDB connection string"
  value       = "mongodb://${var.root_username}:${var.root_password}@${kubernetes_service.mongo.metadata[0].name}:27017/chatApp?authSource=admin"
  sensitive   = true
}
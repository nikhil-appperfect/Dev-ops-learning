variable "namespace" {
  description = "Kubernetes namespace for the MongoDB deployment"
  type        = string
}

variable "image" {
  description = "MongoDB Docker image"
  type        = string
  default     = "mongo"
}

variable "storage_size" {
  description = "Size of the MongoDB persistent volume"
  type        = string
  default     = "5Gi"
}

variable "root_username" {
  description = "MongoDB root username"
  type        = string
  default     = "root"
  sensitive   = true
}

variable "root_password" {
  description = "MongoDB root password"
  type        = string
  default     = "admin"
  sensitive   = true
}
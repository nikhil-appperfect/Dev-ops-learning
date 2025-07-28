variable "namespace" {
  description = "Kubernetes namespace for the backend deployment"
  type        = string
}

variable "image" {
  description = "Backend Docker image"
  type        = string
  default     = "arush75/chat-app-backend:v1"
}

variable "replicas" {
  description = "Number of backend replicas"
  type        = number
  default     = 1
}

variable "port" {
  description = "Backend service port"
  type        = number
  default     = 5001
}

variable "config_map_name" {
  description = "Name of the ConfigMap containing backend configuration"
  type        = string
}

variable "secret_name" {
  description = "Name of the Secret containing backend secrets"
  type        = string
}
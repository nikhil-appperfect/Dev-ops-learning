variable "namespace" {
  description = "Kubernetes namespace for the frontend deployment"
  type        = string
}

variable "image" {
  description = "Frontend Docker image"
  type        = string
  default     = "arush75/chat-app-frontend:v1"
}

variable "replicas" {
  description = "Number of frontend replicas"
  type        = number
  default     = 1
}

variable "port" {
  description = "Frontend service port"
  type        = number
  default     = 80
}

variable "config_map_name" {
  description = "Name of the ConfigMap containing frontend configuration"
  type        = string
}
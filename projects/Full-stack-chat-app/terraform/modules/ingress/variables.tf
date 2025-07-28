
variable "namespace" {
  description = "Kubernetes namespace for the ingress deployment"
  type        = string
  
  validation {
    condition     = can(regex("^[a-z0-9][-a-z0-9]*[a-z0-9]$", var.namespace))
    error_message = "The namespace must consist of lowercase alphanumeric characters or '-', and must start and end with an alphanumeric character."
  }
}

variable "ingress_host" {
  description = "Hostname for the ingress. Not required when using localhost with port forwarding."
  type        = string
  default     = "localhost"
}

variable "frontend_service_name" {
  description = "Name of the frontend service to route traffic to"
  type        = string
}

variable "frontend_service_port" {
  description = "Port of the frontend service"
  type        = number
  
  validation {
    condition     = var.frontend_service_port > 0 && var.frontend_service_port < 65536
    error_message = "The frontend service port must be between 1 and 65535."
  }
}

variable "backend_service_name" {
  description = "Name of the backend service to route API traffic to"
  type        = string
}

variable "backend_service_port" {
  description = "Port of the backend service"
  type        = number
  
  validation {
    condition     = var.backend_service_port > 0 && var.backend_service_port < 65536
    error_message = "The backend service port must be between 1 and 65535."
  }
}
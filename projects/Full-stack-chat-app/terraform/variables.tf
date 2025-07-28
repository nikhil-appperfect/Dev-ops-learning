variable "namespace" {
  description = "Kubernetes namespace for the chat application"
  type        = string
  default     = "chat-app"
}

variable "mongodb" {
  description = "MongoDB configuration"
  type = object({
    image           = string
    storage_size    = string
    root_username   = string
    root_password   = string
  })
  default = {
    image           = "mongo"
    storage_size    = "5Gi"
    root_username   = "root"
    root_password   = "admin"
  }
  sensitive = true
}

variable "backend" {
  description = "Backend configuration"
  type = object({
    image       = string
    replicas    = number
    port        = number
    node_env    = string
  })
  default = {
    image       = "arush75/chat-app-backend:v1"
    replicas    = 1
    port        = 5001
    node_env    = "production"
  }
}

variable "frontend" {
  description = "Frontend configuration"
  type = object({
    image       = string
    replicas    = number
    port        = number
  })
  default = {
    image       = "arush75/chat-app-frontend:v1"
    replicas    = 1
    port        = 80
  }
}

variable "ingress" {
  description = "Ingress configuration"
  type = object({
    enabled     = bool
  })
  default = {
    enabled     = true
  }
}

variable "jwt_secret" {
  description = "JWT secret for backend authentication"
  type        = string
  default     = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
  sensitive   = true
}
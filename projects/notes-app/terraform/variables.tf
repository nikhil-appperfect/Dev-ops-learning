variable "namespace" {
  description = "Kubernetes namespace for the Notes App"
  type        = string
  default     = "notes-app"
}

variable "notes_app_image" {
  description = "Docker image for the Notes App"
  type        = string
  default     = "trainwithshubham/notes-app-k8s"
}

variable "nginx_image" {
  description = "Docker image for Nginx"
  type        = string
  default     = "nginx"
}

variable "notes_app_replicas" {
  description = "Number of replicas for the Notes App deployment"
  type        = number
  default     = 2
}

variable "nginx_replicas" {
  description = "Number of replicas for the Nginx deployment"
  type        = number
  default     = 2
}

variable "notes_app_port" {
  description = "Container port for the Notes App"
  type        = number
  default     = 8000
}

variable "nginx_port" {
  description = "Container port for Nginx"
  type        = number
  default     = 80
}
resource "kubernetes_deployment" "frontend" {
  metadata {
    name      = "chat-app-frontend"
    namespace = var.namespace
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = "chat-app-frontend"
      }
    }

    template {
      metadata {
        labels = {
          app = "chat-app-frontend"
        }
      }

      spec {
        container {
          name  = "chat-app-frontend"
          image = var.image

          port {
            container_port = var.port
          }

          env_from {
            config_map_ref {
              name = var.config_map_name
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "frontend" {
  metadata {
    name      = "frontend"
    namespace = var.namespace
  }

  spec {
    selector = {
      app = "chat-app-frontend"
    }

    port {
      port        = var.port
      target_port = var.port
    }
  }
}
resource "kubernetes_deployment" "backend" {
  metadata {
    name      = "chat-app-backend"
    namespace = var.namespace
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = "chat-app-backend"
      }
    }

    template {
      metadata {
        labels = {
          app = "chat-app-backend"
        }
      }

      spec {
        container {
          name  = "chat-app-backend"
          image = var.image

          port {
            container_port = var.port
          }

          env_from {
            config_map_ref {
              name = var.config_map_name
            }
          }

          env_from {
            secret_ref {
              name = var.secret_name
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "backend" {
  metadata {
    name      = "backend"
    namespace = var.namespace
  }

  spec {
    selector = {
      app = "chat-app-backend"
    }

    port {
      port        = var.port
      target_port = var.port
    }
  }
}
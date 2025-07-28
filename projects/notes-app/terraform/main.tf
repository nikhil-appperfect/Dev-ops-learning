# Create Namespace
resource "kubernetes_namespace" "notes_app" {
  metadata {
    name = var.namespace
  }
}

# Notes App Deployment
resource "kubernetes_deployment" "notes_app" {
  metadata {
    name      = "notes-app-dep"
    namespace = kubernetes_namespace.notes_app.metadata[0].name
  }

  spec {
    replicas = var.notes_app_replicas

    selector {
      match_labels = {
        app = "notes-app"
      }
    }

    template {
      metadata {
        labels = {
          app = "notes-app"
        }
      }

      spec {
        container {
          name  = "notes-app"
          image = var.notes_app_image

          port {
            container_port = var.notes_app_port
          }
        }
      }
    }
  }

  depends_on = [kubernetes_namespace.notes_app]
}

# Notes App Service
resource "kubernetes_service" "notes_app" {
  metadata {
    name      = "notes-app-svc"
    namespace = kubernetes_namespace.notes_app.metadata[0].name
  }

  spec {
    selector = {
      app = "notes-app"
    }

    port {
      port        = 80
      target_port = var.notes_app_port
      protocol    = "TCP"
    }
  }

  depends_on = [kubernetes_deployment.notes_app]
}

# Nginx Deployment
resource "kubernetes_deployment" "nginx" {
  metadata {
    name      = "nginx-dep"
    namespace = kubernetes_namespace.notes_app.metadata[0].name
  }

  spec {
    replicas = var.nginx_replicas

    selector {
      match_labels = {
        app = "nginx"
      }
    }

    template {
      metadata {
        labels = {
          app = "nginx"
        }
      }

      spec {
        container {
          name  = "nginx-pod"
          image = var.nginx_image

          port {
            container_port = var.nginx_port
          }
        }
      }
    }
  }

  depends_on = [kubernetes_namespace.notes_app]
}

# Nginx Service
resource "kubernetes_service" "nginx" {
  metadata {
    name      = "nginx-svc"
    namespace = kubernetes_namespace.notes_app.metadata[0].name
  }

  spec {
    selector = {
      app = "nginx"
    }

    port {
      port        = 80
      target_port = var.nginx_port
      protocol    = "TCP"
    }
  }

  depends_on = [kubernetes_deployment.nginx]
}

# Ingress Resource
resource "kubernetes_ingress_v1" "notes_app_ingress" {
  metadata {
    name      = "notes-app-route"
    namespace = kubernetes_namespace.notes_app.metadata[0].name
    annotations = {
      "nginx.ingress.kubernetes.io/rewrite-target" = "/"
    }
  }

  spec {
    rule {
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.notes_app.metadata[0].name
              port {
                number = 80
              }
            }
          }
        }

        path {
          path      = "/nginx"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.nginx.metadata[0].name
              port {
                number = 80
              }
            }
          }
        }
      }
    }
  }

  depends_on = [
    kubernetes_service.notes_app,
    kubernetes_service.nginx
  ]
}
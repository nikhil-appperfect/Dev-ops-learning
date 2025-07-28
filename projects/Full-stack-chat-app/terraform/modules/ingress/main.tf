resource "null_resource" "enable_ingress_addon" {
  provisioner "local-exec" {
    command = "minikube addons enable ingress"
  }
}

resource "kubernetes_ingress_v1" "chat_app_ingress" {
  metadata {
    name      = "chat-app-ingress"
    namespace = var.namespace
    annotations = {
 
      "kubernetes.io/ingress.class" = "nginx"
      

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
              name = var.frontend_service_name
              port {
                number = var.frontend_service_port
              }
            }
          }
        }
  
        path {
          path      = "/api"
          path_type = "Prefix"
          backend {
            service {
              name = var.backend_service_name
              port {
                number = var.backend_service_port
              }
            }
          }
        }
      }
    }
    
  
  }


  depends_on = [null_resource.enable_ingress_addon]
}
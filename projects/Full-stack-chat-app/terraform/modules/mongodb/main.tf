resource "kubernetes_persistent_volume" "mongodb_pv" {
  metadata {
    name = "mongodb-pv"
  }
  spec {
    capacity = {
      storage = var.storage_size
    }
    access_modes = ["ReadWriteOnce"]
    persistent_volume_source {
      host_path {
        path = "/data"
      }
    }
  }
}

resource "kubernetes_persistent_volume_claim" "mongodb_pvc" {
  metadata {
    name      = "mongodb-pvc"
    namespace = var.namespace
  }
  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = var.storage_size
      }
    }
  }
  depends_on = [kubernetes_persistent_volume.mongodb_pv]
}

resource "kubernetes_deployment" "mongodb" {
  metadata {
    name      = "chat-app-mongodb"
    namespace = var.namespace
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "chat-app-mongodb"
      }
    }

    template {
      metadata {
        labels = {
          app = "chat-app-mongodb"
        }
      }

      spec {
        container {
          name  = "chat-app-mongodb"
          image = var.image

          port {
            container_port = 27017
          }

          env {
            name  = "MONGO_INITDB_ROOT_USERNAME"
            value = var.root_username
          }

          env {
            name  = "MONGO_INITDB_ROOT_PASSWORD"
            value = var.root_password
          }

          volume_mount {
            name       = "mongodb-data"
            mount_path = "/data/db"
          }
        }

        volume {
          name = "mongodb-data"
          persistent_volume_claim {
            claim_name = kubernetes_persistent_volume_claim.mongodb_pvc.metadata[0].name
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "mongo" {
  metadata {
    name      = "mongo"
    namespace = var.namespace
  }

  spec {
    selector = {
      app = "chat-app-mongodb"
    }

    port {
      port        = 27017
      target_port = 27017
    }
  }
}
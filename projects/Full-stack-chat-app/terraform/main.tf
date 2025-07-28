resource "kubernetes_namespace" "chat_app" {
  metadata {
    name = var.namespace
  }
}

resource "kubernetes_config_map" "chat_app_config" {
  metadata {
    name      = "chat-app-config"
    namespace = kubernetes_namespace.chat_app.metadata[0].name
  }

  data = {
    NODE_ENV = var.backend.node_env
    PORT     = tostring(var.backend.port)
  }
}

resource "kubernetes_secret" "chat_app_secret" {
  metadata {
    name      = "chat-app-secret"
    namespace = kubernetes_namespace.chat_app.metadata[0].name
  }

  type = "Opaque"

  data = {
    MONGODB_URI = "mongodb://${var.mongodb.root_username}:${var.mongodb.root_password}@mongo:27017/chatApp?authSource=admin"
    JWT_SECRET  = var.jwt_secret
  }
}

module "mongodb" {
  source = "./modules/mongodb"

  namespace     = kubernetes_namespace.chat_app.metadata[0].name
  image         = var.mongodb.image
  storage_size  = var.mongodb.storage_size
  root_username = var.mongodb.root_username
  root_password = var.mongodb.root_password
}

module "backend" {
  source = "./modules/backend"

  namespace      = kubernetes_namespace.chat_app.metadata[0].name
  image          = var.backend.image
  replicas       = var.backend.replicas
  port           = var.backend.port
  config_map_name = kubernetes_config_map.chat_app_config.metadata[0].name
  secret_name    = kubernetes_secret.chat_app_secret.metadata[0].name

  depends_on = [module.mongodb]
}

module "frontend" {
  source = "./modules/frontend"

  namespace      = kubernetes_namespace.chat_app.metadata[0].name
  image          = var.frontend.image
  replicas       = var.frontend.replicas
  port           = var.frontend.port
  config_map_name = kubernetes_config_map.chat_app_config.metadata[0].name

  depends_on = [module.backend]
}

module "ingress" {
  source = "./modules/ingress"
  count  = var.ingress.enabled ? 1 : 0

  namespace             = kubernetes_namespace.chat_app.metadata[0].name
  frontend_service_name = module.frontend.service_name
  frontend_service_port = module.frontend.service_port
  backend_service_name  = module.backend.service_name
  backend_service_port  = module.backend.service_port

  depends_on = [module.frontend, module.backend]
}
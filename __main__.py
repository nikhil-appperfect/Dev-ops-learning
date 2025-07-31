"""A Kubernetes Python Pulumi program"""

import pulumi
from K8s.namespace import create_domainset
from K8s.service_deployment import create_service_and_deployment
from K8s.volume import create_volume
from K8s.rbac_basic import create_basic_rbac
from K8s.rbac_extended import create_extended_rbac
from K8s.rbac_group_binding import create_group_cluster_role_binding
from K8s.monitoring import create_monitoring_setup
from K8s.prometheus_config import create_prometheus_config
from K8s.logging import (
    log_resource_creation, log_rbac_operation, log_monitoring_setup,
    log_error, project_logger
)

# Initialize logging for the main application
project_logger.app_logger.info("Starting Kubernetes project deployment")

try:
    # Create namespace
    namespace = create_domainset()
    log_resource_creation("namespace", "domainset", namespace="domainset")
    
    # Create service and deployment
    service_deployment = create_service_and_deployment()
    log_resource_creation("service_deployment", "app-service", namespace="domainset")
    
    # Create volume
    volume = create_volume()
    log_resource_creation("volume", "app-volume", namespace="domainset")
    
    # Create RBAC components
    basic_rbac = create_basic_rbac()
    log_rbac_operation("create", "basic-rbac", "ClusterRole", subjects=["default"])
    
    extended_rbac = create_extended_rbac()
    log_rbac_operation("create", "extended-rbac", "ClusterRole", subjects=["admin"])
    
    group_binding = create_group_cluster_role_binding()
    log_rbac_operation("create", "group-binding", "ClusterRoleBinding", subjects=["developers"])
    
    # Create monitoring components
    monitoring = create_monitoring_setup()
    log_monitoring_setup("prometheus", "deployed", namespace="monitoring")
    
    prometheus_config = create_prometheus_config()
    log_monitoring_setup("prometheus-config", "configured", namespace="monitoring")
    
    project_logger.app_logger.info("All Kubernetes resources deployed successfully")
    
except Exception as e:
    log_error(e, "main_deployment")
    project_logger.app_logger.error(f"Deployment failed: {e}")
    raise

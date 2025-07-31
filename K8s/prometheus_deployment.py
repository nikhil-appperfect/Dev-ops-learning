from pulumi_kubernetes.apps.v1 import Deployment
from pulumi_kubernetes.core.v1 import Service, ConfigMap
import pulumi

def create_prometheus_deployment():
    """
    Create Prometheus deployment with web interface to view metrics
    """
    
    # Create ConfigMap for Prometheus configuration
    prometheus_config = ConfigMap('prometheus-config',
        metadata={"namespace": "demo-namespace"},
        data={
            "prometheus.yml": """
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'nginx-metrics'
    static_configs:
      - targets: ['metrics-svc-25ce2371.demo-namespace.svc.cluster.local:9113']
    metrics_path: '/metrics'
    scrape_interval: 30s
    scrape_timeout: 10s
"""
        }
    )

    # Create Prometheus deployment
    prometheus_deployment = Deployment('prometheus',
        metadata={"namespace": "demo-namespace"},
        spec={
            "replicas": 1,
            "selector": {"matchLabels": {"app": "prometheus"}},
            "template": {
                "metadata": {
                    "labels": {"app": "prometheus"},
                    "namespace": "demo-namespace"
                },
                "spec": {
                    "containers": [{
                        "name": "prometheus",
                        "image": "prom/prometheus:latest",
                        "ports": [{"containerPort": 9090}],
                        "args": [
                            "--config.file=/etc/prometheus/prometheus.yml",
                            "--storage.tsdb.path=/prometheus",
                            "--web.console.libraries=/etc/prometheus/console_libraries",
                            "--web.console.templates=/etc/prometheus/consoles",
                            "--storage.tsdb.retention.time=200h",
                            "--web.enable-lifecycle"
                        ],
                        "volumeMounts": [
                            {
                                "name": "prometheus-config",
                                "mountPath": "/etc/prometheus"
                            },
                            {
                                "name": "prometheus-storage",
                                "mountPath": "/prometheus"
                            }
                        ],
                        "resources": {
                            "requests": {
                                "memory": "256Mi",
                                "cpu": "100m"
                            },
                            "limits": {
                                "memory": "512Mi",
                                "cpu": "200m"
                            }
                        }
                    }],
                    "volumes": [
                        {
                            "name": "prometheus-config",
                            "configMap": {
                                "name": "prometheus-config"
                            }
                        },
                        {
                            "name": "prometheus-storage",
                            "emptyDir": {}
                        }
                    ]
                }
            }
        }
    )

    # Create Prometheus service
    prometheus_service = Service('prometheus-svc',
        metadata={"namespace": "demo-namespace"},
        spec={
            "type": "ClusterIP",
            "selector": {"app": "prometheus"},
            "ports": [{"port": 9090, "targetPort": 9090, "name": "http"}]
        })

    # Export the Prometheus deployment and service
    pulumi.export('prometheus_deployment', prometheus_deployment.metadata['name'])
    pulumi.export('prometheus_service', prometheus_service.metadata['name'])
    pulumi.export('prometheus_config', prometheus_config.metadata['name'])
    
    return prometheus_deployment, prometheus_service 
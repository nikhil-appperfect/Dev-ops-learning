from pulumi_kubernetes.apps.v1 import Deployment
from pulumi_kubernetes.core.v1 import Service, ConfigMap
import pulumi

def create_monitoring_setup():
    ConfigMap('nginx-config',
        metadata={"namespace": "demo-namespace"},
        data={
            "nginx.conf": """
events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        location /nginx_status {
            stub_status on;
            access_log off;
            allow all;
        }
    }
}
"""
        }
    )

    # Create deployment with nginx + nginx-exporter for metrics collection
    dep = Deployment('metrics-app',
        metadata={"namespace": "demo-namespace"},
        spec={
            "replicas": 1,
            "selector": {"matchLabels": {"app": "metrics-app"}},
            "template": {
                "metadata": {
                    "labels": {"app": "metrics-app"},
                    "namespace": "demo-namespace"
                },
                "spec": {
                    "containers": [
                        {
                            "name": "nginx",
                            "image": "nginx:alpine",
                            "ports": [{"containerPort": 80}],
                            "volumeMounts": [{
                                "name": "nginx-config",
                                "mountPath": "/etc/nginx/nginx.conf",
                                "subPath": "nginx.conf"
                            }],
                            "resources": {
                                "requests": {
                                    "memory": "64Mi",
                                    "cpu": "50m"
                                },
                                "limits": {
                                    "memory": "128Mi",
                                    "cpu": "100m"
                                }
                            }
                        },
                        {
                            "name": "nginx-exporter",
                            "image": "nginx/nginx-prometheus-exporter:0.11.0",
                            "ports": [{"containerPort": 9113}],
                            "args": ["-nginx.scrape-uri", "http://localhost/nginx_status"],
                            "resources": {
                                "requests": {
                                    "memory": "32Mi",
                                    "cpu": "25m"
                                },
                                "limits": {
                                    "memory": "64Mi",
                                    "cpu": "50m"
                                }
                            }
                        }
                    ],
                    "volumes": [{
                        "name": "nginx-config",
                        "configMap": {
                            "name": "nginx-config-441ca2df"
                        }
                    }]
                }
            }
        }
    )

    # Create service for the nginx application with metrics endpoint
    svc = Service('metrics-svc',
        metadata={"namespace": "demo-namespace"},
        spec={
            "type": "ClusterIP",
            "selector": {"app": "metrics-app"},
            "ports": [
                {"port": 80, "targetPort": 80, "name": "http"},
                {"port": 9113, "targetPort": 9113, "name": "metrics"}
            ]
        })

    pulumi.export('metrics_deployment', dep.metadata['name'])
    pulumi.export('metrics_service', svc.metadata['name'])
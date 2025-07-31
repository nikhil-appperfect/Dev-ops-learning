from pulumi_kubernetes.core.v1 import ConfigMap
from pulumi_kubernetes.apps.v1 import Deployment
from pulumi_kubernetes.core.v1 import Service
import pulumi

def create_prometheus_config():
    """
    Create ServiceMonitor configuration for Prometheus to scrape nginx metrics
    Note: This requires the prometheus-operator to be installed in the cluster
    """
    
    # Create ServiceMonitor using Custom Resource Definition
    # This requires the prometheus-operator to be installed
    service_monitor = {
        "apiVersion": "monitoring.coreos.com/v1",
        "kind": "ServiceMonitor",
        "metadata": {
            "name": "nginx-metrics-monitor",
            "namespace": "demo-namespace",
            "labels": {
                "release": "prometheus",
                "app": "metrics-app"
            }
        },
        "spec": {
            "selector": {
                "matchLabels": {
                    "app": "metrics-app"
                }
            },
            "endpoints": [
                {
                    "port": "metrics",
                    "path": "/metrics",
                    "interval": "30s",
                    "scrapeTimeout": "10s"
                }
            ],
            "namespaceSelector": {
                "matchNames": ["demo-namespace"]
            }
        }
    }
    
    # Create the ServiceMonitor using Pulumi's custom resource
    from pulumi_kubernetes.apiextensions import CustomResource
    
    monitor = CustomResource("nginx-service-monitor",
        api_version="monitoring.coreos.com/v1",
        kind="ServiceMonitor",
        metadata={
            "name": "nginx-metrics-monitor",
            "namespace": "demo-namespace",
            "labels": {
                "release": "prometheus",
                "app": "metrics-app"
            }
        },
        spec={
            "selector": {
                "matchLabels": {
                    "app": "metrics-app"
                }
            },
            "endpoints": [
                {
                    "port": "metrics",
                    "path": "/metrics",
                    "interval": "30s",
                    "scrapeTimeout": "10s"
                }
            ],
            "namespaceSelector": {
                "matchNames": ["demo-namespace"]
            }
        }
    )
    
    # Create PrometheusRule for alerting
    prometheus_rule = CustomResource("nginx-alert-rules",
        api_version="monitoring.coreos.com/v1",
        kind="PrometheusRule",
        metadata={
            "name": "nginx-alert-rules",
            "namespace": "demo-namespace",
            "labels": {
                "release": "prometheus",
                "app": "metrics-app"
            }
        },
        spec={
            "groups": [
                {
                    "name": "nginx.rules",
                    "rules": [
                        {
                            "alert": "NginxDown",
                            "expr": "nginx_up == 0",
                            "for": "1m",
                            "labels": {
                                "severity": "critical"
                            },
                            "annotations": {
                                "summary": "Nginx is down",
                                "description": "Nginx metrics endpoint is not responding"
                            }
                        },
                        {
                            "alert": "HighNginxErrorRate",
                            "expr": "rate(nginx_http_requests_total{status=~\"4..|5..\"}[5m]) > 0.1",
                            "for": "2m",
                            "labels": {
                                "severity": "warning"
                            },
                            "annotations": {
                                "summary": "High nginx error rate",
                                "description": "Nginx is returning high rate of 4xx/5xx errors"
                            }
                        },
                        {
                            "alert": "HighNginxConnectionCount",
                            "expr": "nginx_connections_active > 100",
                            "for": "1m",
                            "labels": {
                                "severity": "warning"
                            },
                            "annotations": {
                                "summary": "High nginx connection count",
                                "description": "Nginx has more than 100 active connections"
                            }
                        }
                    ]
                }
            ]
        }
    )
    
    # Export the ServiceMonitor and PrometheusRule
    pulumi.export('service_monitor', monitor.metadata['name'])
    pulumi.export('prometheus_rule', prometheus_rule.metadata['name'])
    
    return monitor, prometheus_rule 
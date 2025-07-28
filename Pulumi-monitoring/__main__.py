import pulumi
from pulumi_kubernetes.apps.v1 import Deployment
from pulumi_kubernetes.core.v1 import Service
from pulumi_kubernetes.core.v1 import Pod

# Define app labels
app_labels = { "app": "hello-world" }

# -----------------------
# 1. Kubernetes Deployment
# -----------------------
deployment = Deployment("hello-deployment",
    metadata={
        "name": "hello-deployment",
        "labels": app_labels,
        "namespace": "monitoring",
    },
    spec={
        "selector": {
            "matchLabels": app_labels,
        },
        "replicas": 1,
        "template": {
            "metadata": {
                "labels": app_labels,
            },
            "spec": {
                "containers": [{
                    "name": "http-server",
                    "image": "nikhil845/hello-prometheus:latest",
                    "ports": [
                        {"containerPort": 8080},  # HTTP server
                        {"containerPort": 8000},  # Prometheus metrics
                    ],
                }]
            }
        }
    }
)
# -----------------------
# 2. Kubernetes Service
# -----------------------
service = Service("hello-service",
    metadata={
        "name": "hello-service",
        "labels": app_labels,
        "namespace": "monitoring",
    },
    spec={
        "selector": app_labels,
        "ports": [
            {"port": 8080, "targetPort": 8080, "name": "http"},
            {"port": 8000, "targetPort": 8000, "name": "metrics"},
        ],
        "type": "ClusterIP",
    }
)

# -------------------
# 3. Load Generator Pod
# -------------------
# load_generator = Pod("load-generator",
#     metadata={"name": "load-generator", "labels": loader_labels},
#     spec={
#         "containers": [{
#             "name": "curl-loader",
#             "image": "curlimages/curl:latest",  # Lightweight curl image
#             "command": ["/bin/sh", "-c"],
#             "args": ["while true; do curl -s http://hello-service:8080; echo; sleep 4; done"],
#         }]
#     })

loader_labels = { "app": "hello-loader" }

load_generator = Pod("hello-load-generator",
    metadata={
        "name": "hello-load-generator",
        "namespace": "monitoring",
        "labels": loader_labels,
    },
    spec={
        "containers": [{
            "name": "curl-loader",
            "image": "curlimages/curl:latest",
            "command": ["/bin/sh", "-c"],
            "args": [
                "while true; do curl -s http://hello-service:8080 > /dev/null; sleep 2; done"
            ],
        }]
    }
)

# -----------------------
# 3. Export Outputs
# -----------------------
pulumi.export("deployment_name", deployment.metadata["name"])
pulumi.export("service_name", service.metadata["name"])

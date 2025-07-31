from pulumi_kubernetes.apps.v1 import Deployment
from pulumi_kubernetes.core.v1 import Service
import pulumi

def create_service_and_deployment():
    dep = Deployment('hi-dep',
        metadata={"namespace": "demo-namespace"},
        spec={
            "replicas": 2,
            "selector": {"matchLabels": {"app": "myapp"}},
            "template": {
                "metadata": {
                    "labels": {"app": "myapp"},
                    "namespace": "demo-namespace"
                },
                "spec": {
                    "containers": [{
                        "name": "nginx",
                        "image": "nginx:latest",
                        "ports": [{"containerPort": 80}]
                    }]
                }
            }
        }
        )

    svc = Service('hi-svc',
        metadata={"namespace": "demo-namespace"},
        spec={
            "type": "ClusterIP",
            "selector": {"app": "myapp"},
            "ports": [{"port": 80, "targetPort": 80}]
        })

    pulumi.export('deployment', dep.metadata['name'])
    pulumi.export('service', svc.metadata['name'])

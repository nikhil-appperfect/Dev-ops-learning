import pulumi
from pulumi_kubernetes.core.v1 import PersistentVolume, PersistentVolumeClaim, Pod
from K8s.config_secret import create_config_secret_pvc

def create_volume():
    pv = PersistentVolume('app-pv',
        metadata={"namespace": "demo-namespace"},
        spec={
            "capacity": {"storage": "1Gi"},
            "accessModes": ["ReadWriteOnce"],
            "hostPath": {"path": "/mnt/data"}
        })
    pvc = create_config_secret_pvc()

    pod = Pod('app-pod',
        metadata={"namespace": "demo-namespace"},
        spec={
            "containers": [{
                "name": "nginx",
                "image": "nginx",
                "volumeMounts": [{"mountPath": "/usr/share/nginx/html", "name": "data"}]
            }],
            "volumes": [{"name": "data", "persistentVolumeClaim": {"claimName": pvc.metadata["name"]}}]
        })

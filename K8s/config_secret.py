from pulumi_kubernetes.core.v1 import ConfigMap, Secret, PersistentVolumeClaim
import base64

def create_config_secret_pvc():
    cm = ConfigMap('app-config', data={"welcome": "Hello from config!"})
    sec = Secret('app-secret', string_data={"password": "s3cr3tP@ss"})
    pvc = PersistentVolumeClaim('app-pvc',
        metadata={"namespace": "demo-namespace"},
        spec={
            "accessModes": ["ReadWriteOnce"],
            "resources": {"requests": {"storage": "1Gi"}}
        })
    return pvc

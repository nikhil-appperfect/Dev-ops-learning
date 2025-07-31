import pulumi
from pulumi_kubernetes.core.v1 import Namespace

def create_domainset():
    ns = Namespace('demo-ns', metadata={"name": "demo-namespace"})
    pulumi.export('namespace', ns.metadata['name'])

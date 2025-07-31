import pulumi_kubernetes as k8s

def create_multi_namespace_rbac(namespaces=["dev", "qa", "prod"]):
    for ns in namespaces:
        # Make sure namespace exists
        k8s.core.v1.Namespace(ns)

        # Role
        k8s.rbac.v1.Role(f"pod-reader-{ns}",
            metadata={"name": "pod-reader", "namespace": ns},
            rules=[{
                "apiGroups": [""],
                "resources": ["pods"],
                "verbs": ["get", "list"]
            }])

        # ServiceAccount
        sa = k8s.core.v1.ServiceAccount(f"reader-sa-{ns}",
            metadata={"name": "reader-sa", "namespace": ns})

        # RoleBinding
        k8s.rbac.v1.RoleBinding(f"reader-binding-{ns}",
            metadata={"namespace": ns},
            subjects=[{
                "kind": "ServiceAccount",
                "name": sa.metadata["name"],
                "namespace": ns,
            }],
            role_ref={
                "kind": "Role",
                "name": "pod-reader",
                "apiGroup": "rbac.authorization.k8s.io"
            })

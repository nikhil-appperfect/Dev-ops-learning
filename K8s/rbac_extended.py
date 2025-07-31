import pulumi_kubernetes as k8s

def create_extended_rbac(namespace_name="demo-namespace"):
    role = k8s.rbac.v1.Role("resource-editor",
        metadata={"name": "resource-editor", "namespace": namespace_name},
        rules=[{
            "apiGroups": [""],
            "resources": ["pods", "services", "configmaps", "secrets", "persistentvolumeclaims"],
            "verbs": ["get", "list", "watch", "create", "update", "patch", "delete"]
        }])

    sa = k8s.core.v1.ServiceAccount("editor-sa",
        metadata={"name": "editor-sa", "namespace": namespace_name})

    k8s.rbac.v1.RoleBinding("editor-binding",
        metadata={"namespace": namespace_name},
        subjects=[{
            "kind": "ServiceAccount",
            "name": sa.metadata["name"],
            "namespace": namespace_name,
        }],
        role_ref={
            "kind": "Role",
            "name": role.metadata["name"],
            "apiGroup": "rbac.authorization.k8s.io"
        })

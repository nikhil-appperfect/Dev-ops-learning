import pulumi_kubernetes as k8s

def create_basic_rbac(namespace_name="demo-namespace"):
    # Create pod-reader role
    role = k8s.rbac.v1.Role("pod-reader",
        metadata={"name": "pod-reader", "namespace": namespace_name},
        rules=[{
            "apiGroups": [""],
            "resources": ["pods"],
            "verbs": ["list", "watch"]
        }])

    # ServiceAccount
    sa = k8s.core.v1.ServiceAccount("reader-sa",
        metadata={"name": "reader-sa", "namespace": namespace_name})

    # RoleBinding
    k8s.rbac.v1.RoleBinding("reader-binding",
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

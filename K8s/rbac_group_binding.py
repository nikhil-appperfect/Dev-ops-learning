import pulumi_kubernetes as k8s

def create_group_cluster_role_binding():
    cluster_role = k8s.rbac.v1.ClusterRole("read-everything",
        metadata={"namespace": "demo-namespace"},
        rules=[{
            "apiGroups": [""],
            "resources": ["pods", "nodes", "namespaces"],
            "verbs": ["get", "list"]
        }])

    k8s.rbac.v1.ClusterRoleBinding("group-reader-binding",
        metadata={"namespace": "demo-namespace"},
        subjects=[{
            "kind": "Group",
            "name": "devops-group",  # must match external auth group
            "apiGroup": "rbac.authorization.k8s.io"
        }],
        role_ref={
            "kind": "ClusterRole",
            "name": cluster_role.metadata["name"],
            "apiGroup": "rbac.authorization.k8s.io"
        })

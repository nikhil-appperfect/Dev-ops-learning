import * as pulumi from "@pulumi/pulumi";
import * as k8s from "@pulumi/kubernetes";

export interface FrontendArgs {
  namespace: k8s.core.v1.Namespace;
  provider: k8s.Provider;
  backendServiceName: "backend";
}

export class Frontend extends pulumi.ComponentResource {
  public readonly service: k8s.core.v1.Service;

  constructor(name: string, args: FrontendArgs, opts?: pulumi.ComponentResourceOptions) {
    super("custom:resource:Frontend", name, {}, opts);

    const labels = { app: "frontend" };
    const ns = args.namespace.metadata.name;

    const deployment = new k8s.apps.v1.Deployment(`${name}-dep`, {
      metadata: { namespace: ns },
      spec: {
        replicas: 1,
        selector: { matchLabels: labels },
        template: {
          metadata: { labels },
          spec: {
            containers: [{
              name: "frontend",
              image: "nikhil845/chatapp-frontend:latest",
              ports: [{ containerPort : 80 }],
              env: [
                {
                  name: "REACT_APP_API_URL",
                  value: pulumi.interpolate`http://backend:5000`,
                },
              ],
            }],
          },
        },
      },
    }, { provider: args.provider, parent: this });

    this.service = new k8s.core.v1.Service(`${name}-svc`, {
      metadata: { namespace: ns },
      spec: {
        type: "NodePort",
        ports: [{ port: 80, targetPort: 80, nodePort: 30080 }], // 👈 Fix targetPort
        selector: labels,
      },
    }, { provider: args.provider, parent: this });
    

    this.registerOutputs({ service: this.service });
  }
}

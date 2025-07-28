import * as pulumi from "@pulumi/pulumi";
import * as k8s from "@pulumi/kubernetes";

export interface BackendArgs {
  namespace: k8s.core.v1.Namespace;
  provider: k8s.Provider;
  mongoStatefulSetName: pulumi.Input<string>;
  mongoHeadlessServiceName: pulumi.Input<string>;
}

export class Backend extends pulumi.ComponentResource {
  public readonly service: k8s.core.v1.Service;

  constructor(name: string, args: BackendArgs, opts?: pulumi.ComponentResourceOptions) {
    super("custom:resource:Backend", name, {}, opts);

    const labels = { app: "backend" };
    const ns = args.namespace.metadata.name;

    // Compose MongoDB URI with StatefulSet pods and headless service DNS names
    const mongoUri = pulumi.interpolate`mongodb://mongodbadmin:secret@${args.mongoStatefulSetName}-0.${args.mongoHeadlessServiceName}.${ns}.svc.cluster.local:27017,${args.mongoStatefulSetName}-1.${args.mongoHeadlessServiceName}.${ns}.svc.cluster.local:27017,${args.mongoStatefulSetName}-2.${args.mongoHeadlessServiceName}.${ns}.svc.cluster.local:27017/chatapp?replicaSet=rs0&authSource=admin`;

    // Create Deployment
    const deployment = new k8s.apps.v1.Deployment(`${name}-dep`, {
      metadata: { namespace: ns },
      spec: {
        replicas: 1,
        selector: { matchLabels: labels },
        template: {
          metadata: { labels },
          spec: {
            containers: [{
              name: "backend",
              image: "nikhil845/chatapp-backend:latest",
              ports: [{ containerPort: 5000 }],
              env: [
                // Use secret references to pull env vars from chatapp-secret
                {
                  name: "MONGODB_URI",
                  valueFrom: {
                    secretKeyRef: {
                      name: "chatapp-secret",
                      key: "MONGODB_URI",
                    },
                  },
                },
                {
                  name: "JWT_SECRET",
                  valueFrom: {
                    secretKeyRef: {
                      name: "chatapp-secret",
                      key: "JWT_SECRET",
                    },
                  },
                },
                {
                  name: "PORT",
                  valueFrom: {
                    secretKeyRef: {
                      name: "chatapp-secret",
                      key: "PORT",
                    },
                  },
                },
                {
                  name: "NODE_ENV",
                  valueFrom: {
                    secretKeyRef: {
                      name: "chatapp-secret",
                      key: "NODE_ENV",
                    },
                  },
                },
              ],
            }],
          },
        },
      },
    }, { provider: args.provider, parent: this });

    // Create Service for backend
    this.service = new k8s.core.v1.Service(`${name}-svc`, {
      metadata: {
        namespace: ns,
        name: "backend",
      },
      spec: {
        selector: labels,
        ports: [{ port: 5000, targetPort: 5000 }],
        type: "ClusterIP",
      },
    }, { provider: args.provider, parent: this });

    this.registerOutputs({
      service: this.service,
      deployment,
    });
  }
}

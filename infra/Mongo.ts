import * as pulumi from "@pulumi/pulumi";
import * as k8s from "@pulumi/kubernetes";

export interface MongoArgs {
  namespace: k8s.core.v1.Namespace;
  provider: k8s.Provider;
}

export class Mongo extends pulumi.ComponentResource {
  public readonly svc: k8s.core.v1.Service;
  public readonly headlessSvc: k8s.core.v1.Service;
  public readonly sts: k8s.apps.v1.StatefulSet;

  constructor(name: string, args: MongoArgs, opts?: pulumi.ComponentResourceOptions) {
    super("custom:resource:MongoReplicaSet", name, {}, opts);

    const labels = { app: "mongo" };

    this.headlessSvc = new k8s.core.v1.Service(`${name}-headless`, {
      metadata: {
        namespace: args.namespace.metadata.name,
        name: `${name}-headless`,
      },
      spec: {
        clusterIP: "None",
        selector: labels,
        ports: [{ port: 27017, targetPort: 27017 }],
      },
    }, { provider: args.provider, parent: this });

    this.svc = new k8s.core.v1.Service(`${name}-svc`, {
      metadata: {
        namespace: args.namespace.metadata.name,
        name: `${name}-svc`,
      },
      spec: {
        selector: labels,
        ports: [{ port: 27017, targetPort: 27017 }],
      },
    }, { provider: args.provider, parent: this });

    this.sts = new k8s.apps.v1.StatefulSet(`${name}-sts`, {
      metadata: {
        namespace: args.namespace.metadata.name,
        name: `${name}-sts`,
      },
      spec: {
        serviceName: this.headlessSvc.metadata.name,
        replicas: 3,
        selector: { matchLabels: labels },
        template: {
          metadata: { labels },
          spec: {
            containers: [{
              name: "mongo",
              image: "mongo:4.4",
              command: ["mongod", "--replSet", "rs0", "--bind_ip_all"],
              ports: [{ containerPort: 27017 }],
              env: [
                { name: "MONGO_INITDB_ROOT_USERNAME", value: "mongodbadmin" },
                { name: "MONGO_INITDB_ROOT_PASSWORD", value: "secret" },
              ],
              volumeMounts: [{
                name: "mongo-data",
                mountPath: "/data/db",
              }],
            }],
          },
        },
        volumeClaimTemplates: [{
          metadata: { name: "mongo-data" },
          spec: {
            accessModes: ["ReadWriteOnce"],
            resources: { requests: { storage: "1Gi" } },
            storageClassName: "standard",
          },
        }],
      },
    }, { provider: args.provider, parent: this });

    this.registerOutputs({
      svc: this.svc,
      headlessSvc: this.headlessSvc,
      sts: this.sts,
    });
  }
}

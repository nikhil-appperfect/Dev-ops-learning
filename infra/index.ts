import * as pulumi from "@pulumi/pulumi";
import * as k8s from "@pulumi/kubernetes";

import { Mongo } from "./Mongo";
import { Backend } from "./backend";
import { Frontend } from "./frontend";

const provider = new k8s.Provider("k8s", {
  kubeconfig: process.env.KUBECONFIG,
});

// Create namespace
const ns = new k8s.core.v1.Namespace("chat-app", {
  metadata: { name: "chat-app" },
}, { provider });

// MongoDB replica set
const mongo = new Mongo("mongo", {
  namespace: ns,
  provider,
});

// Backend, passes mongo StatefulSet and headless service names
const backend = new Backend("backend", {
  namespace: ns,
  provider,
  mongoStatefulSetName: mongo.sts.metadata.name,
  mongoHeadlessServiceName: mongo.headlessSvc.metadata.name,
});

// Frontend, points to backend service
const frontend = new Frontend("frontend", {
  namespace: ns,
  provider,
  backendServiceName: "backend",
});

// Export services' cluster IPs or names if needed
export const frontendSvcName = frontend.service.metadata.name;
export const backendSvcName = backend.service.metadata.name;
export const mongoSvcName = mongo.svc.metadata.name;

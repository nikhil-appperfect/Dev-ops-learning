# Notes App Terraform Deployment

This directory contains Terraform configuration to deploy the Notes App on Kubernetes (Minikube).

## Prerequisites

- Terraform installed (version >= 1.0.0)
- Minikube installed and running
- kubectl configured to work with Minikube

## Files Structure

- `main.tf` - Main Terraform configuration file
- `variables.tf` - Variable definitions
- `outputs.tf` - Output definitions
- `providers.tf` - Provider configuration

## How to Use

### Initialize Terraform

```bash
terraform init
```

### Plan the Deployment

```bash
terraform plan
```

### Apply the Configuration

```bash
terraform apply
```

### Access the Application

After applying the Terraform configuration, run the following command to access the application:

```bash
kubectl port-forward svc/ingress-nginx-controller 8080:80 -n ingress-nginx --address=0.0.0.0
```

Then access:
- Notes App: http://localhost:8080
- Nginx: http://localhost:8080/nginx

### Destroy the Infrastructure

When you're done, you can destroy all the resources created by Terraform:

```bash
terraform destroy
```
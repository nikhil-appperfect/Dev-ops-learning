# 🚀 Kubernetes Infrastructure as Code with Monitoring Stack

A comprehensive Kubernetes infrastructure project demonstrating RBAC, monitoring with Prometheus/Grafana, and Infrastructure as Code using Pulumi.

## 📋 Project Overview

This project showcases a complete Kubernetes infrastructure setup including:
- **RBAC (Role-Based Access Control)** implementation
- **Monitoring stack** with Prometheus and Grafana
- **Infrastructure as Code** using Pulumi
- **Service deployments** and namespace management
- **Resource management** and storage configuration

## 🏗️ Architecture

```
final-project/
├── K8s/                          # Kubernetes configurations
│   ├── namespace.py              # Namespace management
│   ├── rbac_basic.py            # Basic RBAC implementation
│   ├── rbac_extended.py         # Extended RBAC features
│   ├── rbac_multi_namespace.py  # Multi-namespace RBAC
│   ├── rbac_group_binding.py    # Group-based RBAC
│   ├── service_deployment.py    # Service deployment
│   ├── volume.py                # Storage configuration
│   ├── config_secret.py         # Secret management
│   ├── prometheus_config.py     # Prometheus configuration
│   ├── prometheus_deployment.py # Prometheus deployment
│   └── servicemonitor.yaml      # ServiceMonitor for metrics
├── __main__.py                   # Main application entry point
├── Pulumi.yaml                   # Pulumi project configuration
├── requirements.txt              # Python dependencies
├── values.yaml                   # Helm values for monitoring
└── README.md                     # Project documentation
```

## 🎯 Key Features

### 🔐 **RBAC Implementation**
- **Service Accounts**: Dedicated service accounts for applications
- **Role Definitions**: ClusterRoles and Roles with specific permissions
- **Role Bindings**: Proper binding of roles to service accounts
- **Group Access**: Group-based cluster role bindings
- **Multi-namespace**: Cross-namespace permission management
- **Resource-specific**: Granular access control for pods, services, secrets

### 📊 **Monitoring Stack**
- **Prometheus**: Metrics collection and storage
- **Grafana**: Dashboard visualization and alerting
- **ServiceMonitor**: Automatic service discovery
- **Custom Metrics**: Application-specific monitoring
- **Alert Rules**: Health monitoring and alerting

### 🏗️ **Infrastructure as Code**
- **Pulumi**: Python-based infrastructure definition
- **Resource Management**: Automated resource provisioning
- **Configuration**: Environment-specific configurations
- **State Management**: Pulumi state storage and management

### 🚀 **Service Management**
- **Namespace Management**: Automated namespace creation
- **Deployment Templates**: Reusable deployment configurations
- **Service Definitions**: Automated service creation
- **Storage Management**: Persistent volume management

## 🛠️ Prerequisites

- **Kubernetes Cluster**: Minikube or any Kubernetes cluster
- **Python 3.9+**: For Pulumi and application code
- **kubectl**: Kubernetes command-line tool
- **Helm**: For Prometheus/Grafana deployment
- **Pulumi CLI**: For infrastructure management

## 📦 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd final-project
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Pulumi
```bash
curl -fsSL https://get.pulumi.com | sh
export PATH="$PATH:$HOME/.pulumi/bin"
```

### 4. Configure Kubernetes
```bash
# Start Minikube (if using local cluster)
minikube start

# Verify cluster access
kubectl cluster-info
```

## 🚀 Quick Start

### 1. Deploy Infrastructure with Pulumi
```bash
# Initialize Pulumi stack
pulumi stack init dev

# Deploy infrastructure
pulumi up --yes
```

### 2. Deploy Monitoring Stack
```bash
# Add Prometheus Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Deploy Prometheus and Grafana
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  -f values.yaml
```

### 3. Apply RBAC Configurations
```bash
# Deploy RBAC configurations
python3 __main__.py
```

## 📊 Monitoring

### Access Grafana Dashboard
```bash
# Port forward Grafana service
kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring

# Access at http://localhost:3000
# Default credentials: admin / prom-operator
```

### Access Prometheus
```bash
# Port forward Prometheus service
kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090 -n monitoring

# Access at http://localhost:9090
```

## 🔐 RBAC Components

### Basic RBAC
- **Service Accounts**: Application-specific service accounts
- **Roles**: Namespace-level permissions
- **Role Bindings**: Binding roles to service accounts

### Extended RBAC
- **Cluster Roles**: Cluster-wide permissions
- **Group Bindings**: Group-based access control
- **Multi-namespace**: Cross-namespace access management

### Security Features
- **Resource Quotas**: Resource limits and requests
- **Network Policies**: Network access control
- **Pod Security**: Pod security standards

## 📈 Monitoring Features

### Prometheus Configuration
- **Service Discovery**: Automatic service discovery
- **Custom Metrics**: Application-specific metrics
- **Alert Rules**: Health monitoring rules
- **Data Retention**: Configurable data retention

### Grafana Dashboards
- **Cluster Overview**: Overall cluster health
- **Application Metrics**: Application-specific dashboards
- **Resource Usage**: CPU, memory, storage monitoring
- **Custom Panels**: Configurable monitoring panels

## 🛠️ Development

### Project Structure
```
K8s/
├── namespace.py              # Namespace management
├── rbac_*.py               # RBAC implementations
├── service_deployment.py    # Service deployment
├── volume.py               # Storage configuration
├── prometheus_*.py         # Prometheus configurations
└── servicemonitor.yaml     # ServiceMonitor
```

### Adding New Components
1. **Create Python module** in `K8s/` directory
2. **Define Pulumi resources** using Python SDK
3. **Update main application** in `__main__.py`
4. **Test deployment** with `pulumi preview`

## 🔧 Configuration

### Environment Variables
```bash
export KUBECONFIG=~/.kube/config
export PULUMI_ACCESS_TOKEN=your-access-token
export PULUMI_ORG=your-organization
```

### Pulumi Configuration
```bash
# Set configuration values
pulumi config set kubernetes:replicas 3
pulumi config set monitoring:enabled true
pulumi config set logging:level INFO
```

## 📚 Documentation

### RBAC Implementation
- **Basic RBAC**: `K8s/rbac_basic.py`
- **Extended RBAC**: `K8s/rbac_extended.py`
- **Multi-namespace**: `K8s/rbac_multi_namespace.py`
- **Group Bindings**: `K8s/rbac_group_binding.py`

### Monitoring Setup
- **Prometheus Config**: `K8s/prometheus_config.py`
- **Prometheus Deployment**: `K8s/prometheus_deployment.py`
- **ServiceMonitor**: `K8s/servicemonitor.yaml`

### Infrastructure
- **Namespace Management**: `K8s/namespace.py`
- **Service Deployment**: `K8s/service_deployment.py`
- **Storage Configuration**: `K8s/volume.py`
- **Secret Management**: `K8s/config_secret.py`

## 🚀 Deployment

### Development Environment
```bash
pulumi stack select dev
pulumi up --yes
```

### Production Environment
```bash
pulumi stack select production
pulumi config set kubernetes:replicas 5
pulumi config set monitoring:enabled true
pulumi up --yes
```

## 🔍 Troubleshooting

### Common Issues
1. **RBAC Permissions**: Check service account permissions
2. **Monitoring Access**: Verify Grafana/Prometheus access
3. **Resource Limits**: Check resource quotas and limits
4. **Network Policies**: Verify network connectivity

### Debug Commands
```bash
# Check RBAC
kubectl get clusterroles,clusterrolebindings
kubectl get roles,rolebindings --all-namespaces

# Check Monitoring
kubectl get pods -n monitoring
kubectl get svc -n monitoring

# Check Pulumi State
pulumi stack --show-urns
pulumi preview
```


**Built with ❤️ using Kubernetes, Pulumi, Prometheus, and Grafana**

# 🚀 Kubernetes Infrastructure as Code with Pulumi

A comprehensive Kubernetes project that demonstrates Infrastructure as Code (IaC) using Pulumi Python SDK. This project includes complete Kubernetes infrastructure setup with monitoring, logging, RBAC, and comprehensive logging collection.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Components](#components)
- [Logging System](#logging-system)
- [Monitoring](#monitoring)
- [RBAC Configuration](#rbac-configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 Overview

This project demonstrates a complete Kubernetes infrastructure setup using Pulumi with Python. It includes:

- **Infrastructure as Code**: Complete Kubernetes resources defined in Python
- **Monitoring Stack**: Prometheus, Grafana, and Loki for observability
- **RBAC Management**: Comprehensive role-based access control
- **Logging System**: Automated log collection and analysis
- **Volume Management**: Persistent storage configuration
- **Service Mesh**: Basic service deployment and networking

## ✨ Features

### 🔧 Core Infrastructure
- ✅ **Namespace Management**: Custom namespace creation and management
- ✅ **Service Deployment**: Nginx-based application deployment
- ✅ **Volume Management**: Persistent volumes and claims
- ✅ **ConfigMaps & Secrets**: Configuration management
- ✅ **RBAC**: Role-based access control with multiple levels

### 📊 Monitoring & Observability
- ✅ **Prometheus**: Metrics collection and alerting
- ✅ **Grafana**: Dashboard and visualization
- ✅ **Loki**: Log aggregation and querying
- ✅ **ServiceMonitor**: Custom resource for service monitoring
- ✅ **Alert Rules**: PrometheusRule for alerting

### 🔐 Security & Access Control
- ✅ **Basic RBAC**: Pod reader roles and bindings
- ✅ **Extended RBAC**: Resource editor roles
- ✅ **Cluster RBAC**: Cluster-wide role bindings
- ✅ **Service Accounts**: Managed service accounts

### 📝 Logging & Analysis
- ✅ **Comprehensive Logging**: Multi-component logging system
- ✅ **Automated Collection**: Scripts for log gathering
- ✅ **Structured Logs**: JSON format for analysis
- ✅ **Real-time Monitoring**: Live log following
- ✅ **Error Tracking**: Detailed error logging with context

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │   Demo      │  │  Monitoring │  │   System    │       │
│  │ Namespace   │  │  Namespace  │  │  Namespace  │       │
│  │             │  │             │  │             │       │
│  │ • Nginx App │  │ • Prometheus│  │ • CoreDNS   │       │
│  │ • Services  │  │ • Grafana   │  │ • etcd      │       │
│  │ • Volumes   │  │ • Loki      │  │ • kubelet   │       │
│  │ • RBAC      │  │ • AlertMgr  │  │ • scheduler │       │
│  └─────────────┘  └─────────────┘  └─────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Pulumi Infrastructure                    │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │   Python    │  │   Logging   │  │  Collection │       │
│  │   Code      │  │   System    │  │   Scripts   │       │
│  │             │  │             │  │             │       │
│  │ • Resources │  │ • Multi-    │  │ • kubectl   │       │
│  │ • Deploy    │  │   component │  │ • Pulumi    │       │
│  │ • Configure │  │ • Structured│  │ • Monitoring│       │
│  └─────────────┘  └─────────────┘  └─────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

### Required Software
- **Python 3.8+**: For Pulumi Python SDK
- **Pulumi CLI**: Infrastructure as Code tool
- **kubectl**: Kubernetes command-line tool
- **Docker**: Container runtime (optional)
- **Helm**: Package manager for Kubernetes (optional)

### Required Access
- **Kubernetes Cluster**: Access to a Kubernetes cluster
- **Admin Permissions**: For RBAC and namespace creation
- **Storage**: For persistent volumes

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd final-project
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Install Pulumi CLI
```bash
# macOS
brew install pulumi

# Linux
curl -fsSL https://get.pulumi.com | sh

# Windows
choco install pulumi
```

### 4. Configure Kubernetes Access
```bash
# Ensure kubectl is configured
kubectl cluster-info

# Verify access
kubectl get nodes
```

## 🎮 Usage

### Quick Start

1. **Initialize Pulumi Stack**
```bash
pulumi stack init dev
```

2. **Deploy Infrastructure**
```bash
pulumi up
```

3. **View Resources**
```bash
pulumi stack output
```

4. **Access Applications**
```bash
# Get service URLs
kubectl get svc -n demo-namespace

# Access monitoring
kubectl port-forward svc/prometheus-service 9090:9090 -n monitoring
```

### Logging System Usage

1. **Collect All Logs**
```bash
python run_log_collection.py
```

2. **View Log Summary**
```bash
python run_log_collection.py --summary-only
```

3. **List Log Files**
```bash
python run_log_collection.py --list-files
```

4. **Test Logging System**
```bash
python test_logging.py
```

## 📁 Project Structure

```
final-project/
├── 📄 __main__.py                 # Main Pulumi program
├── 📄 Pulumi.yaml                 # Pulumi project configuration
├── 📄 requirements.txt             # Python dependencies
├── 📄 values.yaml                 # Helm values configuration
├── 📄 .gitignore                  # Git ignore rules
│
├── 📁 K8s/                        # Kubernetes components
│   ├── 📄 namespace.py            # Namespace creation
│   ├── 📄 service_deployment.py   # Service and deployment
│   ├── 📄 volume.py              # Volume management
│   ├── 📄 rbac_basic.py          # Basic RBAC
│   ├── 📄 rbac_extended.py       # Extended RBAC
│   ├── 📄 rbac_group_binding.py  # Cluster RBAC
│   ├── 📄 monitoring.py          # Monitoring setup
│   ├── 📄 prometheus_config.py   # Prometheus configuration
│   ├── 📄 prometheus_deployment.py # Prometheus deployment
│   ├── 📄 config_secret.py       # ConfigMaps and secrets
│   ├── 📄 logging.py             # Logging system
│   ├── 📄 get_helm.sh           # Helm installation script
│   └── 📄 servicemonitor.yaml   # ServiceMonitor CRD
│
├── 📁 logs/                       # Generated log files
│   ├── 📄 application.log        # Application logs
│   ├── 📄 kubernetes.log         # Kubernetes operations
│   ├── 📄 rbac.log              # RBAC operations
│   ├── 📄 monitoring.log        # Monitoring logs
│   ├── 📄 errors.log            # Error logs
│   └── 📄 structured_logs.json  # Structured JSON logs
│
├── 📁 test_logs/                 # Test log collection
│   ├── 📄 cluster_roles.json    # Cluster roles data
│   ├── 📄 cluster_role_bindings.json # RBAC bindings
│   ├── 📄 kubernetes_events.json # Kubernetes events
│   └── 📄 pod_*.log             # Individual pod logs
│
├── 📄 log_collector.py           # Log collection script
├── 📄 run_log_collection.py      # Log collection runner
├── 📄 test_logging.py           # Logging test script
└── 📄 LOGGING_README.md         # Logging documentation
```

## 🔧 Components

### 1. Namespace Management (`K8s/namespace.py`)
Creates a custom namespace for the application:
```python
def create_domainset():
    ns = Namespace('demo-ns', metadata={"name": "demo-namespace"})
    pulumi.export('namespace', ns.metadata['name'])
```

### 2. Service Deployment (`K8s/service_deployment.py`)
Deploys Nginx application with service:
- **Deployment**: 2 replicas of Nginx
- **Service**: ClusterIP service exposing port 80
- **Labels**: Proper labeling for service discovery

### 3. Volume Management (`K8s/volume.py`)
Manages persistent storage:
- **PersistentVolume**: HostPath-based storage
- **PersistentVolumeClaim**: Storage requests
- **Pod**: Application using persistent storage

### 4. RBAC Configuration

#### Basic RBAC (`K8s/rbac_basic.py`)
- **Role**: Pod reader permissions
- **ServiceAccount**: Managed service account
- **RoleBinding**: Binds role to service account

#### Extended RBAC (`K8s/rbac_extended.py`)
- **Role**: Resource editor with full CRUD permissions
- **Resources**: Pods, services, configmaps, secrets, PVCs
- **Verbs**: get, list, watch, create, update, patch, delete

#### Cluster RBAC (`K8s/rbac_group_binding.py`)
- **ClusterRole**: Read-only cluster-wide permissions
- **ClusterRoleBinding**: Binds to external groups
- **Scope**: Cluster-wide access control

### 5. Monitoring Stack

#### Monitoring Setup (`K8s/monitoring.py`)
- **Nginx with Exporter**: Application with metrics endpoint
- **ConfigMap**: Nginx configuration
- **Service**: Exposes both app and metrics ports
- **Resources**: CPU and memory limits

#### Prometheus Configuration (`K8s/prometheus_config.py`)
- **ServiceMonitor**: Custom resource for service monitoring
- **PrometheusRule**: Alert rules for Nginx
- **Endpoints**: Metrics scraping configuration
- **Labels**: Proper labeling for discovery

### 6. Configuration Management (`K8s/config_secret.py`)
- **ConfigMap**: Application configuration
- **Secret**: Sensitive data (base64 encoded)
- **PVC**: Persistent volume claims

## 📝 Logging System

### Features
- **Multi-component logging**: Separate loggers for different components
- **Structured logging**: JSON format for machine-readable logs
- **File-based storage**: Organized log files
- **Error tracking**: Comprehensive error logging with context
- **Automated collection**: Scripts for log gathering

### Log Files
```
logs/
├── application.log          # Main application logs
├── kubernetes.log          # Kubernetes operations
├── rbac.log               # RBAC operations
├── monitoring.log          # Monitoring component logs
├── errors.log             # Error logs
├── structured_logs.json   # Structured JSON logs
└── collection_log.json    # Log collection summary
```

### Usage Examples

#### Basic Log Collection
```bash
python run_log_collection.py
```

#### Custom Directory
```bash
python run_log_collection.py --log-dir /path/to/logs
```

#### View Summary
```bash
python run_log_collection.py --summary-only
```

#### Real-time Logs
```bash
# Follow application logs
tail -f logs/application.log

# Follow error logs
tail -f logs/errors.log
```

## 📊 Monitoring

### Prometheus Setup
- **Metrics Collection**: Scrapes Nginx metrics
- **Alert Rules**: NginxDown alerts
- **Service Discovery**: Automatic target discovery
- **Dashboard**: Grafana integration

### Grafana Integration
- **Data Sources**: Prometheus and Loki
- **Dashboards**: Pre-configured dashboards
- **Alerts**: Visual alert management

### Loki Log Aggregation
- **Log Collection**: Centralized log storage
- **Query Interface**: LogQL for log queries
- **Integration**: Grafana integration for logs

## 🔐 RBAC Configuration

### Permission Levels

#### 1. Basic Access (Pod Reader)
```yaml
apiGroups: [""]
resources: ["pods"]
verbs: ["list", "watch"]
```

#### 2. Extended Access (Resource Editor)
```yaml
apiGroups: [""]
resources: ["pods", "services", "configmaps", "secrets", "persistentvolumeclaims"]
verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
```

#### 3. Cluster Access (Read Everything)
```yaml
apiGroups: [""]
resources: ["pods", "nodes", "namespaces"]
verbs: ["get", "list"]
```

### Service Accounts
- **reader-sa**: Basic pod reading permissions
- **editor-sa**: Full resource management permissions
- **Group Bindings**: External group integration

## 🛠️ Troubleshooting

### Common Issues

#### 1. Pulumi Authentication
```bash
# Login to Pulumi
pulumi login

# Check current user
pulumi whoami
```

#### 2. Kubernetes Access
```bash
# Test cluster access
kubectl cluster-info

# Check nodes
kubectl get nodes
```

#### 3. Resource Quotas
```bash
# Check resource quotas
kubectl get resourcequota -n demo-namespace

# Check limits
kubectl describe limitrange -n demo-namespace
```

#### 4. Log Collection Issues
```bash
# Check kubectl access
kubectl get pods --all-namespaces

# Test log collection
python test_logging.py
```

### Debug Commands

#### Pulumi Debug
```bash
# Preview changes
pulumi preview

# Show stack info
pulumi stack output

# Show resources
pulumi stack --show-urns
```

#### Kubernetes Debug
```bash
# Check pod status
kubectl get pods -n demo-namespace

# Check events
kubectl get events -n demo-namespace

# Check logs
kubectl logs <pod-name> -n demo-namespace
```

#### Logging Debug
```bash
# Check log files
ls -la logs/

# View structured logs
cat logs/structured_logs.json | jq '.'

# Test logging
python test_logging.py
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Style
- Follow Python PEP 8 guidelines
- Add docstrings to functions
- Include type hints
- Write meaningful commit messages

### Testing
```bash
# Test logging system
python test_logging.py

# Test log collection
python run_log_collection.py --summary-only

# Test Pulumi deployment
pulumi preview
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Pulumi Team**: For the excellent IaC platform
- **Kubernetes Community**: For the robust container orchestration
- **Prometheus Team**: For the monitoring solution
- **Grafana Team**: For the visualization platform

---

## 📞 Support

For questions, issues, or contributions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the logging documentation
- Test with the provided scripts

**Happy Kubernetes Infrastructure as Code! 🚀** 
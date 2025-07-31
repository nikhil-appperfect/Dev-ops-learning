#!/usr/bin/env python3
"""
Log Collection Script for Kubernetes Project
Collects and stores logs from various project components
"""

import os
import sys
import json
import subprocess
import datetime
from pathlib import Path
from typing import Dict, List, Any
import pulumi
from K8s.logging import (
    log_resource_creation, log_rbac_operation, log_monitoring_setup,
    log_error, log_pulumi_output, get_log_summary, project_logger
)


class LogCollector:
    """Collects logs from various sources in the Kubernetes project"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.collection_log = self.log_dir / "collection_log.json"
        
    def collect_pulumi_logs(self):
        """Collect logs from Pulumi operations"""
        try:
            # Get Pulumi stack info
            result = subprocess.run(
                ["pulumi", "stack", "export"], 
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                stack_data = json.loads(result.stdout)
                log_pulumi_output("stack_export", stack_data)
                project_logger.app_logger.info("Successfully collected Pulumi stack logs")
            else:
                log_error(Exception(f"Pulumi stack export failed: {result.stderr}"), "pulumi_export")
                
        except Exception as e:
            log_error(e, "pulumi_logs_collection")
    
    def collect_kubectl_logs(self, namespace: str = None):
        """Collect logs from kubectl commands"""
        try:
            # Get all pods
            cmd = ["kubectl", "get", "pods", "--all-namespaces", "-o", "json"]
            if namespace:
                cmd = ["kubectl", "get", "pods", "-n", namespace, "-o", "json"]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                pods_data = json.loads(result.stdout)
                log_pulumi_output("kubectl_pods", pods_data)
                
                # Collect logs from each pod
                for item in pods_data.get("items", []):
                    pod_name = item["metadata"]["name"]
                    pod_namespace = item["metadata"]["namespace"]
                    
                    # Get pod logs
                    log_cmd = ["kubectl", "logs", pod_name, "-n", pod_namespace]
                    log_result = subprocess.run(log_cmd, capture_output=True, text=True)
                    
                    if log_result.returncode == 0:
                        log_file = self.log_dir / f"pod_{pod_name}_{pod_namespace}.log"
                        with open(log_file, 'w') as f:
                            f.write(log_result.stdout)
                        project_logger.k8s_logger.info(f"Collected logs for pod {pod_name} in {pod_namespace}")
                    else:
                        log_error(Exception(f"Failed to get logs for pod {pod_name}: {log_result.stderr}"), "kubectl_logs")
                        
            else:
                log_error(Exception(f"kubectl get pods failed: {result.stderr}"), "kubectl_pods")
                
        except Exception as e:
            log_error(e, "kubectl_logs_collection")
    
    def collect_system_logs(self):
        """Collect system-level logs"""
        try:
            # Get Kubernetes events
            result = subprocess.run(
                ["kubectl", "get", "events", "--all-namespaces", "-o", "json"],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                events_data = json.loads(result.stdout)
                log_pulumi_output("kubernetes_events", events_data)
                
                # Save events to file
                events_file = self.log_dir / "kubernetes_events.json"
                with open(events_file, 'w') as f:
                    json.dump(events_data, f, indent=2)
                    
                project_logger.k8s_logger.info("Successfully collected Kubernetes events")
            else:
                log_error(Exception(f"Failed to get Kubernetes events: {result.stderr}"), "kubernetes_events")
                
        except Exception as e:
            log_error(e, "system_logs_collection")
    
    def collect_monitoring_logs(self):
        """Collect logs from monitoring components"""
        try:
            # Check if Prometheus is running
            result = subprocess.run(
                ["kubectl", "get", "pods", "-n", "monitoring", "-l", "app=prometheus", "-o", "json"],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                prometheus_pods = json.loads(result.stdout)
                log_monitoring_setup("prometheus", "running", pod_count=len(prometheus_pods.get("items", [])))
                
                # Get Prometheus logs
                for item in prometheus_pods.get("items", []):
                    pod_name = item["metadata"]["name"]
                    log_cmd = ["kubectl", "logs", pod_name, "-n", "monitoring"]
                    log_result = subprocess.run(log_cmd, capture_output=True, text=True)
                    
                    if log_result.returncode == 0:
                        log_file = self.log_dir / f"prometheus_{pod_name}.log"
                        with open(log_file, 'w') as f:
                            f.write(log_result.stdout)
                        project_logger.monitoring_logger.info(f"Collected Prometheus logs from {pod_name}")
                        
            else:
                log_monitoring_setup("prometheus", "not_found")
                
        except Exception as e:
            log_error(e, "monitoring_logs_collection")
    
    def collect_rbac_logs(self):
        """Collect RBAC-related logs"""
        try:
            # Get ClusterRoles
            result = subprocess.run(
                ["kubectl", "get", "clusterroles", "-o", "json"],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                cluster_roles = json.loads(result.stdout)
                log_rbac_operation("list", "clusterroles", "ClusterRole", 
                                 subjects=[role["metadata"]["name"] for role in cluster_roles.get("items", [])])
                
                # Save to file
                rbac_file = self.log_dir / "cluster_roles.json"
                with open(rbac_file, 'w') as f:
                    json.dump(cluster_roles, f, indent=2)
                    
            # Get ClusterRoleBindings
            result = subprocess.run(
                ["kubectl", "get", "clusterrolebindings", "-o", "json"],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                cluster_role_bindings = json.loads(result.stdout)
                log_rbac_operation("list", "clusterrolebindings", "ClusterRoleBinding",
                                 subjects=[binding["metadata"]["name"] for binding in cluster_role_bindings.get("items", [])])
                
                # Save to file
                rbac_file = self.log_dir / "cluster_role_bindings.json"
                with open(rbac_file, 'w') as f:
                    json.dump(cluster_role_bindings, f, indent=2)
                    
        except Exception as e:
            log_error(e, "rbac_logs_collection")
    
    def collect_all_logs(self):
        """Collect all available logs"""
        collection_start = datetime.datetime.now()
        
        project_logger.app_logger.info("Starting comprehensive log collection")
        
        # Collect different types of logs
        self.collect_pulumi_logs()
        self.collect_kubectl_logs()
        self.collect_system_logs()
        self.collect_monitoring_logs()
        self.collect_rbac_logs()
        
        collection_end = datetime.datetime.now()
        duration = (collection_end - collection_start).total_seconds()
        
        # Log collection summary
        summary = get_log_summary()
        summary["collection_duration_seconds"] = duration
        summary["collection_timestamp"] = collection_end.isoformat()
        
        # Save collection summary
        with open(self.collection_log, 'w') as f:
            json.dump(summary, f, indent=2)
        
        project_logger.app_logger.info(f"Log collection completed in {duration:.2f} seconds")
        project_logger.app_logger.info(f"Logs stored in: {self.log_dir}")
        
        return summary


def main():
    """Main function to run log collection"""
    collector = LogCollector()
    
    try:
        summary = collector.collect_all_logs()
        print(f"Log collection completed successfully!")
        print(f"Logs stored in: {collector.log_dir}")
        print(f"Collection summary: {json.dumps(summary, indent=2)}")
        
    except Exception as e:
        log_error(e, "main_log_collection")
        print(f"Error during log collection: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 
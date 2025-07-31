"""
Logging module for Kubernetes project
Collects and stores logs from various project components
"""

import os
import logging
import json
import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import pulumi
from pulumi import Output


class ProjectLogger:
    """Centralized logging for the Kubernetes project"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup file handlers
        self.setup_loggers()
        
    def setup_loggers(self):
        """Setup different loggers for different components"""
        # Main application logger
        self.app_logger = self._create_logger(
            "app", 
            self.log_dir / "application.log"
        )
        
        # Kubernetes operations logger
        self.k8s_logger = self._create_logger(
            "kubernetes", 
            self.log_dir / "kubernetes.log"
        )
        
        # RBAC operations logger
        self.rbac_logger = self._create_logger(
            "rbac", 
            self.log_dir / "rbac.log"
        )
        
        # Monitoring operations logger
        self.monitoring_logger = self._create_logger(
            "monitoring", 
            self.log_dir / "monitoring.log"
        )
        
        # Error logger
        self.error_logger = self._create_logger(
            "errors", 
            self.log_dir / "errors.log"
        )
        
    def _create_logger(self, name: str, log_file: Path) -> logging.Logger:
        """Create a logger with file and console handlers"""
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def log_resource_creation(self, resource_type: str, resource_name: str, 
                            namespace: Optional[str] = None, **kwargs):
        """Log resource creation events"""
        message = f"Creating {resource_type}: {resource_name}"
        if namespace:
            message += f" in namespace: {namespace}"
        
        self.k8s_logger.info(message)
        self._log_structured_data("resource_creation", {
            "resource_type": resource_type,
            "resource_name": resource_name,
            "namespace": namespace,
            "timestamp": datetime.datetime.now().isoformat(),
            **kwargs
        })
    
    def log_rbac_operation(self, operation: str, role_name: str, 
                          role_type: str, subjects: list = None):
        """Log RBAC operations"""
        message = f"RBAC {operation}: {role_type} '{role_name}'"
        if subjects:
            message += f" for subjects: {subjects}"
        
        self.rbac_logger.info(message)
        self._log_structured_data("rbac_operation", {
            "operation": operation,
            "role_name": role_name,
            "role_type": role_type,
            "subjects": subjects,
            "timestamp": datetime.datetime.now().isoformat()
        })
    
    def log_monitoring_setup(self, component: str, status: str, **kwargs):
        """Log monitoring component setup"""
        message = f"Monitoring {component}: {status}"
        self.monitoring_logger.info(message)
        self._log_structured_data("monitoring_setup", {
            "component": component,
            "status": status,
            "timestamp": datetime.datetime.now().isoformat(),
            **kwargs
        })
    
    def log_error(self, error: Exception, context: str = "", **kwargs):
        """Log errors with context"""
        error_message = f"Error in {context}: {str(error)}"
        self.error_logger.error(error_message, exc_info=True)
        self._log_structured_data("error", {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            "timestamp": datetime.datetime.now().isoformat(),
            **kwargs
        })
    
    def log_pulumi_output(self, resource_name: str, output_data: Any):
        """Log Pulumi resource outputs"""
        self.app_logger.info(f"Pulumi output for {resource_name}: {output_data}")
        self._log_structured_data("pulumi_output", {
            "resource_name": resource_name,
            "output_data": str(output_data),
            "timestamp": datetime.datetime.now().isoformat()
        })
    
    def _log_structured_data(self, event_type: str, data: Dict[str, Any]):
        """Log structured data to JSON file"""
        json_log_file = self.log_dir / "structured_logs.json"
        
        log_entry = {
            "event_type": event_type,
            "data": data
        }
        
        try:
            # Append to JSON log file
            with open(json_log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            self.error_logger.error(f"Failed to write structured log: {e}")
    
    def get_log_summary(self) -> Dict[str, Any]:
        """Generate a summary of all logs"""
        summary = {
            "log_directory": str(self.log_dir),
            "log_files": [],
            "total_entries": 0
        }
        
        for log_file in self.log_dir.glob("*.log"):
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    summary["log_files"].append({
                        "name": log_file.name,
                        "size_bytes": log_file.stat().st_size,
                        "line_count": len(lines)
                    })
                    summary["total_entries"] += len(lines)
            except Exception as e:
                self.error_logger.error(f"Failed to read log file {log_file}: {e}")
        
        return summary


# Global logger instance
project_logger = ProjectLogger()


def log_resource_creation(resource_type: str, resource_name: str, 
                         namespace: Optional[str] = None, **kwargs):
    """Convenience function to log resource creation"""
    project_logger.log_resource_creation(resource_type, resource_name, namespace, **kwargs)


def log_rbac_operation(operation: str, role_name: str, role_type: str, 
                      subjects: list = None):
    """Convenience function to log RBAC operations"""
    project_logger.log_rbac_operation(operation, role_name, role_type, subjects)


def log_monitoring_setup(component: str, status: str, **kwargs):
    """Convenience function to log monitoring setup"""
    project_logger.log_monitoring_setup(component, status, **kwargs)


def log_error(error: Exception, context: str = "", **kwargs):
    """Convenience function to log errors"""
    project_logger.log_error(error, context, **kwargs)


def log_pulumi_output(resource_name: str, output_data: Any):
    """Convenience function to log Pulumi outputs"""
    project_logger.log_pulumi_output(resource_name, output_data)


def get_log_summary() -> Dict[str, Any]:
    """Get a summary of all collected logs"""
    return project_logger.get_log_summary() 
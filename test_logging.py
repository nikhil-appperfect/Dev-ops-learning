#!/usr/bin/env python3
"""
Test script to demonstrate logging functionality
"""

import sys
import time
from K8s.logging import (
    log_resource_creation, log_rbac_operation, log_monitoring_setup,
    log_error, log_pulumi_output, get_log_summary, project_logger
)


def test_logging_functionality():
    """Test all logging functions"""
    
    print("🧪 Testing logging functionality...")
    
    # Test resource creation logging
    log_resource_creation("pod", "test-pod", namespace="test-namespace", 
                         image="nginx:latest", replicas=3)
    
    # Test RBAC logging
    log_rbac_operation("create", "test-role", "ClusterRole", 
                      subjects=["test-user", "test-group"])
    
    # Test monitoring logging
    log_monitoring_setup("prometheus", "deployed", namespace="monitoring", 
                        version="v2.45.0")
    
    # Test Pulumi output logging
    log_pulumi_output("test-resource", {"status": "created", "id": "test-123"})
    
    # Test error logging
    try:
        raise ValueError("This is a test error")
    except Exception as e:
        log_error(e, "test_function")
    
    # Test application logging
    project_logger.app_logger.info("Test application log message")
    project_logger.k8s_logger.info("Test Kubernetes log message")
    project_logger.rbac_logger.info("Test RBAC log message")
    project_logger.monitoring_logger.info("Test monitoring log message")
    
    print("✅ Logging tests completed!")
    
    # Get and display log summary
    summary = get_log_summary()
    print(f"\n📊 Log Summary:")
    print(f"   Log directory: {summary['log_directory']}")
    print(f"   Total entries: {summary['total_entries']}")
    print(f"   Log files: {len(summary['log_files'])}")
    
    for log_file in summary['log_files']:
        print(f"   - {log_file['name']}: {log_file['line_count']} lines, {log_file['size_bytes']} bytes")


def test_log_collection():
    """Test log collection functionality"""
    
    print("\n🔍 Testing log collection...")
    
    try:
        from log_collector import LogCollector
        
        # Create a test collector
        collector = LogCollector("test_logs")
        
        # Test collection (this will fail gracefully if kubectl/pulumi not available)
        try:
            summary = collector.collect_all_logs()
            print(f"✅ Log collection completed!")
            print(f"   Duration: {summary.get('collection_duration_seconds', 0):.2f} seconds")
        except Exception as e:
            print(f"⚠️  Log collection failed (expected if kubectl/pulumi not configured): {e}")
            
    except ImportError as e:
        print(f"❌ Could not import log collector: {e}")


def main():
    """Main test function"""
    
    print("🚀 Starting logging system tests...")
    print("=" * 50)
    
    # Test basic logging
    test_logging_functionality()
    
    # Test log collection
    test_log_collection()
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed!")
    print("\n📁 Check the 'logs' directory for generated log files:")
    print("   - application.log")
    print("   - kubernetes.log") 
    print("   - rbac.log")
    print("   - monitoring.log")
    print("   - errors.log")
    print("   - structured_logs.json")


if __name__ == "__main__":
    main() 
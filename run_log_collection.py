#!/usr/bin/env python3
"""
Simple script to run log collection with different options
"""

import argparse
import json
import sys
from pathlib import Path
from log_collector import LogCollector
from K8s.logging import get_log_summary


def main():
    parser = argparse.ArgumentParser(description="Collect logs from Kubernetes project")
    parser.add_argument("--log-dir", default="logs", help="Directory to store logs")
    parser.add_argument("--namespace", help="Specific namespace to collect logs from")
    parser.add_argument("--summary-only", action="store_true", help="Only show log summary")
    parser.add_argument("--list-files", action="store_true", help="List all log files")
    
    args = parser.parse_args()
    
    if args.summary_only:
        # Just show existing log summary
        summary = get_log_summary()
        print(json.dumps(summary, indent=2))
        return
    
    if args.list_files:
        # List all log files
        log_dir = Path(args.log_dir)
        if log_dir.exists():
            print(f"Log files in {log_dir}:")
            for log_file in log_dir.glob("*"):
                if log_file.is_file():
                    size = log_file.stat().st_size
                    print(f"  {log_file.name} ({size} bytes)")
        else:
            print(f"Log directory {log_dir} does not exist")
        return
    
    # Run full log collection
    collector = LogCollector(args.log_dir)
    
    try:
        summary = collector.collect_all_logs()
        print(f"\n✅ Log collection completed successfully!")
        print(f"📁 Logs stored in: {collector.log_dir}")
        print(f"📊 Total log entries: {summary.get('total_entries', 0)}")
        print(f"⏱️  Collection time: {summary.get('collection_duration_seconds', 0):.2f} seconds")
        
        # Show log files created
        print(f"\n📋 Log files created:")
        for log_file in summary.get('log_files', []):
            print(f"  - {log_file['name']} ({log_file['line_count']} lines, {log_file['size_bytes']} bytes)")
            
    except Exception as e:
        print(f"❌ Error during log collection: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 
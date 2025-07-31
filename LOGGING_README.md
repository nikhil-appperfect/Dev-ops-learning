# Kubernetes Project Logging System

This project includes a comprehensive logging system that collects and stores logs from various Kubernetes components and Pulumi operations.

## Features

- **Multi-component logging**: Separate loggers for different components (Kubernetes, RBAC, Monitoring, etc.)
- **Structured logging**: JSON format for machine-readable logs
- **File-based storage**: All logs stored in organized files
- **Error tracking**: Comprehensive error logging with context
- **Log collection**: Automated collection from kubectl, Pulumi, and monitoring components

## Log Files Structure

```
logs/
├── application.log          # Main application logs
├── kubernetes.log          # Kubernetes operations
├── rbac.log               # RBAC operations
├── monitoring.log          # Monitoring component logs
├── errors.log             # Error logs
├── structured_logs.json   # Structured JSON logs
├── collection_log.json    # Log collection summary
├── kubernetes_events.json # Kubernetes events
├── cluster_roles.json     # Cluster roles data
├── cluster_role_bindings.json # Cluster role bindings data
└── pod_*.log             # Individual pod logs
```

## Usage

### 1. Basic Log Collection

Run the log collection script to gather all available logs:

```bash
python run_log_collection.py
```

### 2. Custom Log Directory

Specify a custom directory for logs:

```bash
python run_log_collection.py --log-dir /path/to/logs
```

### 3. Namespace-Specific Collection

Collect logs from a specific namespace:

```bash
python run_log_collection.py --namespace monitoring
```

### 4. View Log Summary

Get a summary of existing logs:

```bash
python run_log_collection.py --summary-only
```

### 5. List Log Files

List all available log files:

```bash
python run_log_collection.py --list-files
```

## Integration with Pulumi

The logging system is integrated with your Pulumi deployment. When you run:

```bash
pulumi up
```

The system will automatically log:
- Resource creation events
- RBAC operations
- Monitoring setup
- Errors and exceptions

## Log Types

### 1. Application Logs (`application.log`)
- Pulumi deployment progress
- Resource creation events
- Application startup/shutdown

### 2. Kubernetes Logs (`kubernetes.log`)
- Pod creation and management
- Service deployments
- Volume operations
- Namespace operations

### 3. RBAC Logs (`rbac.log`)
- ClusterRole creation
- ClusterRoleBinding operations
- Role assignments
- Permission changes

### 4. Monitoring Logs (`monitoring.log`)
- Prometheus deployment
- ServiceMonitor creation
- Monitoring configuration
- Alert setup

### 5. Error Logs (`errors.log`)
- Exception details
- Error context
- Stack traces
- Recovery attempts

### 6. Structured Logs (`structured_logs.json`)
Machine-readable logs in JSON format for:
- Resource creation events
- RBAC operations
- Monitoring setup
- Error events
- Pulumi outputs

## Log Collection Components

The log collector gathers information from:

1. **Pulumi Stack**: Current stack state and resources
2. **Kubernetes Pods**: All pod logs across namespaces
3. **Kubernetes Events**: System events and notifications
4. **RBAC Resources**: ClusterRoles and ClusterRoleBindings
5. **Monitoring Components**: Prometheus and related services

## Example Output

```
✅ Log collection completed successfully!
📁 Logs stored in: logs
📊 Total log entries: 156
⏱️  Collection time: 12.34 seconds

📋 Log files created:
  - application.log (45 lines, 2048 bytes)
  - kubernetes.log (67 lines, 3072 bytes)
  - rbac.log (23 lines, 1024 bytes)
  - monitoring.log (34 lines, 1536 bytes)
  - errors.log (12 lines, 512 bytes)
  - structured_logs.json (89 lines, 4096 bytes)
```

## Monitoring and Analysis

### View Real-time Logs

```bash
# Follow application logs
tail -f logs/application.log

# Follow error logs
tail -f logs/errors.log

# Follow Kubernetes logs
tail -f logs/kubernetes.log
```

### Analyze Structured Logs

```bash
# View structured logs
cat logs/structured_logs.json | jq '.'

# Filter by event type
cat logs/structured_logs.json | jq 'select(.event_type == "resource_creation")'

# Get recent errors
cat logs/structured_logs.json | jq 'select(.event_type == "error") | .data'
```

### Log Rotation

The logging system doesn't automatically rotate logs. For production use, consider:

1. **Manual rotation**: Archive old logs periodically
2. **Log rotation tools**: Use `logrotate` or similar
3. **Cloud logging**: Send logs to cloud logging services

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure write permissions to log directory
2. **kubectl not found**: Install kubectl and configure access
3. **Pulumi not configured**: Run `pulumi login` and configure stack

### Debug Mode

Enable debug logging by modifying the logging level in `K8s/logging.py`:

```python
logger.setLevel(logging.DEBUG)  # Change from INFO to DEBUG
```

## Customization

### Adding New Log Types

1. Add new logger in `K8s/logging.py`:
```python
self.custom_logger = self._create_logger("custom", self.log_dir / "custom.log")
```

2. Add logging function:
```python
def log_custom_event(self, event_type: str, data: dict):
    self.custom_logger.info(f"Custom event: {event_type}")
    self._log_structured_data("custom_event", data)
```

### Custom Log Formats

Modify the formatter in `_create_logger()` method to change log format:

```python
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
```

## Security Considerations

- Log files may contain sensitive information
- Ensure log directory has appropriate permissions
- Consider encrypting log files in production
- Regularly review and clean old logs
- Don't commit log files to version control

## Performance

- Log collection is designed to be non-intrusive
- Large log files may impact performance
- Consider log rotation for long-running systems
- Monitor disk space usage in log directory 
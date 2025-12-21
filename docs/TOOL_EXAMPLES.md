# FTL Tools Examples

This document provides practical examples of using ftl-tools for common infrastructure automation tasks.

## Getting Started

### Basic Tool Usage

```python
import ftl_automation

# Simple localhost example
localhost_inventory = {
    "all": {
        "hosts": {
            "localhost": {
                "ansible_connection": "local"
            }
        }
    }
}

with ftl_automation.automation(
    inventory=localhost_inventory,
    tools=["hostname", "service"]
) as ftl:
    # Set hostname
    result = ftl.hostname(name="my-server")
    print(f"Hostname changed: {result.get('changed')}")
```

## System Administration

### User Management

```python
# Create users and manage SSH access
with ftl_automation.automation(
    inventory="production.yml",
    tools=["user", "authorized_key"]
) as ftl:
    # Create application user
    ftl.user(
        name="appuser",
        state="present",
        shell="/bin/bash",
        groups="wheel"
    )
    
    # Add SSH public key
    ftl.authorized_key(
        user="appuser",
        key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ... user@workstation",
        state="present"
    )
    
    # Create service user (no shell)
    ftl.user(
        name="nginx", 
        state="present",
        shell="/bin/false",
        system=True
    )
```

### Service Management

```python
# Manage system services
with ftl_automation.automation(
    inventory="servers.yml",
    tools=["service", "systemd_service"]
) as ftl:
    # Start and enable nginx
    ftl.service(name="nginx", state="started")
    ftl.systemd_service(name="nginx", enabled=True)
    
    # Restart application service
    ftl.service(name="myapp", state="restarted")
    
    # Stop and disable unused service
    ftl.service(name="unused-service", state="stopped")
    ftl.systemd_service(name="unused-service", enabled=False)
```

## Package Management

### Multi-Distribution Package Installation

```python
# Install packages on different distributions
with ftl_automation.automation(
    inventory="mixed_servers.yml",
    tools=["dnf", "apt"]
) as ftl:
    # For RHEL/Fedora systems (using dnf)
    ftl.dnf(name="nginx", state="present")
    ftl.dnf(name="git", state="latest")
    
    # For Debian/Ubuntu systems (using apt) 
    ftl.apt(name="nginx", state="present")
    ftl.apt(name="git", state="latest")
    
    # Update all packages
    ftl.dnf(name="*", state="latest")  # RHEL/Fedora
    ftl.apt(name="*", state="latest")  # Debian/Ubuntu
```

### Python Package Management

```python
# Manage Python packages
with ftl_automation.automation(
    inventory="python_servers.yml",
    tools=["pip"]
) as ftl:
    # Install application dependencies
    packages = ["django", "requests", "psycopg2-binary"]
    
    for package in packages:
        ftl.pip(name=package, state="present")
    
    # Install specific version
    ftl.pip(name="django", state="present", version="4.2.0")
    
    # Remove unused package
    ftl.pip(name="old-package", state="absent")
```

## File Operations

### Configuration File Management

```python
# Manage configuration files
with ftl_automation.automation(
    inventory="web_servers.yml", 
    tools=["copy", "lineinfile", "chmod", "chown"]
) as ftl:
    # Copy main configuration
    ftl.copy(
        src="nginx.conf",
        dest="/etc/nginx/nginx.conf",
        backup=True
    )
    
    # Modify specific setting
    ftl.lineinfile(
        path="/etc/nginx/nginx.conf",
        line="worker_processes auto;",
        regexp="^worker_processes"
    )
    
    # Set correct permissions
    ftl.chmod(path="/etc/nginx/nginx.conf", mode="0644")
    ftl.chown(path="/etc/nginx/nginx.conf", owner="root", group="root")
    
    # Create application directory
    ftl.mkdir(path="/opt/myapp", mode="0755")
    ftl.chown(path="/opt/myapp", owner="appuser", group="appuser")
```

### Template Processing

```python
# Use Jinja2 templates for configuration
with ftl_automation.automation(
    inventory="database_servers.yml",
    tools=["template", "service"]
) as ftl:
    # Process database configuration template
    ftl.template(
        src="postgresql.conf.j2",
        dest="/etc/postgresql/15/main/postgresql.conf",
        variables={
            "max_connections": 200,
            "shared_buffers": "256MB",
            "listen_addresses": "*"
        }
    )
    
    # Restart service to apply changes
    ftl.service(name="postgresql", state="restarted")
```

### File Downloads

```python
# Download and manage files
with ftl_automation.automation(
    inventory="app_servers.yml",
    tools=["get_url", "unarchive", "chown"]
) as ftl:
    # Download application archive
    ftl.get_url(
        url="https://releases.example.com/myapp-1.2.3.tar.gz",
        dest="/tmp/myapp-1.2.3.tar.gz"
    )
    
    # Extract to application directory
    ftl.unarchive(
        src="/tmp/myapp-1.2.3.tar.gz",
        dest="/opt/myapp",
        owner="appuser",
        group="appuser"
    )
    
    # Clean up
    ftl.file(path="/tmp/myapp-1.2.3.tar.gz", state="absent")
```

## Network & Security

### Firewall Configuration

```python
# Configure firewall rules
with ftl_automation.automation(
    inventory="production_servers.yml",
    tools=["firewalld"]
) as ftl:
    # Enable basic services
    ftl.firewalld(service="ssh", state="enabled", permanent=True)
    ftl.firewalld(service="http", state="enabled", permanent=True) 
    ftl.firewalld(service="https", state="enabled", permanent=True)
    
    # Open custom application ports
    ftl.firewalld(port="8080/tcp", state="enabled", permanent=True)
    ftl.firewalld(port="9000/tcp", state="enabled", permanent=True)
    
    # Remove unused rules
    ftl.firewalld(service="ftp", state="disabled", permanent=True)
```

### SSL Certificate Management

```python
# Manage SSL certificates with Let's Encrypt
with ftl_automation.automation(
    inventory="web_servers.yml",
    tools=["certbot", "service"]
) as ftl:
    # Obtain SSL certificate
    ftl.certbot(
        domains=["example.com", "www.example.com"],
        email="admin@example.com",
        webroot_path="/var/www/html"
    )
    
    # Reload nginx to use new certificate
    ftl.service(name="nginx", state="reloaded")
```

## Container Management

### Podman Operations

```python
# Manage containers with Podman
with ftl_automation.automation(
    inventory="container_hosts.yml",
    tools=["podman"]
) as ftl:
    # Pull latest images
    images = ["nginx:latest", "postgres:15", "redis:alpine"]
    
    for image in images:
        ftl.podman(action="pull", image=image)
    
    # Run web server container
    ftl.podman(
        action="run",
        image="nginx:latest",
        name="web-server",
        ports=["80:80", "443:443"],
        volumes=["/opt/webapp:/usr/share/nginx/html:ro"]
    )
    
    # Run database container
    ftl.podman(
        action="run",
        image="postgres:15",
        name="database",
        environment={
            "POSTGRES_DB": "myapp",
            "POSTGRES_USER": "appuser", 
            "POSTGRES_PASSWORD": "secure_password"
        },
        volumes=["/opt/pgdata:/var/lib/postgresql/data"]
    )
```

## Development Workflows

### Git Repository Management

```python
# Manage Git repositories
with ftl_automation.automation(
    inventory="dev_servers.yml",
    tools=["git", "chown"]
) as ftl:
    # Clone application repository
    ftl.git(
        repo="https://github.com/company/myapp.git",
        dest="/opt/myapp",
        version="main"
    )
    
    # Set ownership for application user
    ftl.chown(
        path="/opt/myapp",
        owner="appuser",
        group="appuser",
        recurse=True
    )
    
    # Deploy specific version
    ftl.git(
        repo="https://github.com/company/myapp.git", 
        dest="/opt/myapp",
        version="v1.2.3"
    )
```

### Java Application Deployment

```python
# Deploy Java applications
with ftl_automation.automation(
    inventory="java_servers.yml", 
    tools=["java_jar", "systemd_service", "copy"]
) as ftl:
    # Copy application JAR
    ftl.copy(
        src="myapp-1.0.0.jar",
        dest="/opt/myapp/myapp.jar",
        owner="appuser", 
        group="appuser"
    )
    
    # Create systemd service for Java app
    service_content = """[Unit]
Description=My Java Application
After=network.target

[Service] 
Type=simple
User=appuser
Group=appuser
ExecStart=/usr/bin/java -jar /opt/myapp/myapp.jar
Restart=always

[Install]
WantedBy=multi-user.target"""
    
    ftl.copy(
        content=service_content,
        dest="/etc/systemd/system/myapp.service"
    )
    
    # Enable and start service
    ftl.systemd_service(name="myapp", enabled=True)
    ftl.service(name="myapp", state="started")
```

## Communication & Monitoring

### Notification Systems

```python
# Send notifications during deployment
with ftl_automation.automation(
    inventory="all_servers.yml",
    tools=["slack", "discord"]
) as ftl:
    # Notify start of deployment
    ftl.slack(
        channel="#deployments",
        message="🚀 Starting deployment to production servers",
        token="xoxb-your-slack-token"
    )
    
    # ... deployment tasks ...
    
    # Notify completion
    ftl.discord(
        webhook_url="https://discord.com/api/webhooks/...",
        content="✅ Deployment completed successfully!"
    )
```

## Complex Workflows

### Complete Web Application Setup

```python
# Complete web application deployment
with ftl_automation.automation(
    inventory="production.yml",
    tools=[
        "dnf", "user", "authorized_key", "git", "copy",
        "service", "firewalld", "certbot", "slack"
    ]
) as ftl:
    # System preparation
    ftl.dnf(name="nginx", state="present")
    ftl.dnf(name="git", state="present")
    
    # User setup
    ftl.user(name="webapp", state="present", groups="nginx")
    ftl.authorized_key(
        user="webapp",
        key="ssh-rsa AAAAB3NzaC1yc2E...",
        state="present"
    )
    
    # Application deployment
    ftl.git(
        repo="https://github.com/company/webapp.git",
        dest="/opt/webapp",
        version="production"
    )
    
    # Configuration
    ftl.copy(
        src="nginx-webapp.conf", 
        dest="/etc/nginx/conf.d/webapp.conf"
    )
    
    # Services
    ftl.service(name="nginx", state="started")
    ftl.service(name="nginx", state="enabled")
    
    # Security
    ftl.firewalld(service="http", state="enabled", permanent=True)
    ftl.firewalld(service="https", state="enabled", permanent=True)
    
    ftl.certbot(
        domains=["webapp.example.com"],
        email="admin@example.com"
    )
    
    # Notification
    ftl.slack(
        channel="#deployments",
        message="🎉 Web application deployed successfully!",
        token="xoxb-token"
    )
```

### Database Server Setup

```python
# Complete database server configuration
with ftl_automation.automation(
    inventory="database_servers.yml",
    tools=[
        "dnf", "user", "service", "copy", "chmod", 
        "firewalld", "lineinfile"
    ]
) as ftl:
    # Install PostgreSQL
    ftl.dnf(name="postgresql-server", state="present")
    ftl.dnf(name="postgresql-contrib", state="present")
    
    # Initialize database
    ftl.bash(command="postgresql-setup --initdb")
    
    # Configure authentication
    ftl.lineinfile(
        path="/var/lib/pgsql/data/pg_hba.conf",
        line="host    all         all         192.168.1.0/24    md5",
        insertafter="# IPv4 local connections:"
    )
    
    # Configure PostgreSQL settings
    ftl.lineinfile(
        path="/var/lib/pgsql/data/postgresql.conf",
        line="listen_addresses = '*'",
        regexp="^#?listen_addresses"
    )
    
    # Set permissions
    ftl.chmod(path="/var/lib/pgsql/data", mode="0700")
    ftl.chown(path="/var/lib/pgsql/data", owner="postgres", group="postgres")
    
    # Start services
    ftl.service(name="postgresql", state="started")
    ftl.service(name="postgresql", state="enabled")
    
    # Configure firewall
    ftl.firewalld(port="5432/tcp", state="enabled", permanent=True)
```

## Error Handling and Validation

### Robust Deployment Script

```python
# Deployment with error handling
with ftl_automation.automation(
    inventory="production.yml",
    tools=["service", "git", "slack"]
) as ftl:
    try:
        # Stop application
        stop_result = ftl.service(name="myapp", state="stopped")
        
        # Update code
        git_result = ftl.git(
            repo="https://github.com/company/myapp.git",
            dest="/opt/myapp", 
            version="production"
        )
        
        # Start application
        start_result = ftl.service(name="myapp", state="started")
        
        # Verify service is running
        status_result = ftl.bash(command="systemctl is-active myapp")
        
        if status_result.get("stdout", "").strip() == "active":
            ftl.slack(
                channel="#deployments",
                message="✅ Deployment successful - service is active",
                token="xoxb-token"
            )
        else:
            raise Exception("Service failed to start")
            
    except Exception as e:
        # Rollback on failure
        ftl.service(name="myapp", state="stopped")
        ftl.git(
            repo="https://github.com/company/myapp.git",
            dest="/opt/myapp",
            version="previous-stable"
        )
        ftl.service(name="myapp", state="started")
        
        ftl.slack(
            channel="#deployments", 
            message=f"❌ Deployment failed: {e}. Rolled back to previous version.",
            token="xoxb-token"
        )
```

## Tips and Best Practices

### 1. Use Inventory Variables

```yaml
# inventory.yml
all:
  hosts:
    web1.example.com:
      app_version: "1.2.3"
      max_connections: 100
    web2.example.com: 
      app_version: "1.2.3"
      max_connections: 200
```

```python
# Use variables in automation
with ftl_automation.automation(inventory="inventory.yml") as ftl:
    # Variables are accessible through context
    version = ftl.context.inventory["all"]["hosts"]["web1.example.com"]["app_version"]
```

### 2. Conditional Operations

```python
# Check system state before operations
with ftl_automation.automation(inventory="servers.yml", tools=["bash", "service"]) as ftl:
    # Check if service exists
    check_result = ftl.bash(command="systemctl list-unit-files myapp.service")
    
    if check_result.get("rc") == 0:
        ftl.service(name="myapp", state="restarted")
    else:
        print("Service myapp not found, skipping restart")
```

### 3. Batch Operations

```python
# Process multiple items efficiently
servers = ["web1", "web2", "web3"]
packages = ["nginx", "git", "htop"]

with ftl_automation.automation(inventory="inventory.yml", tools=["dnf"]) as ftl:
    for package in packages:
        ftl.dnf(name=package, state="present")
```

### 4. Environment-Specific Configuration

```python
import os

environment = os.getenv("ENVIRONMENT", "development")
inventory_file = f"inventory-{environment}.yml"

with ftl_automation.automation(
    inventory=inventory_file,
    tools=["copy", "service"]
) as ftl:
    # Deploy environment-specific configuration
    ftl.copy(
        src=f"config-{environment}.conf",
        dest="/etc/myapp/config.conf"
    )
```

These examples demonstrate the flexibility and power of ftl-tools for infrastructure automation. Start with simple examples and gradually build more complex workflows as you become familiar with the tools.
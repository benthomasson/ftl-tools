# FTL Tools Reference

This document provides comprehensive documentation for all available tools in the ftl-tools package. Tools are simplified interfaces to FTL modules designed for AI agents and automation systems.

## Tool Categories

### 🏢 System Administration

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| **hostname** | Set system hostname | `name` (string) |
| **service** | Manage system services | `name`, `state` (started/stopped/restarted) |
| **user** | Manage user accounts | `name`, `state`, `groups`, `shell` |
| **timezone** | Configure system timezone | `name` (timezone string) |

### 📦 Package Management

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| **dnf** | Manage RPM packages (Fedora/RHEL) | `name`, `state` (present/absent/latest) |
| **apt** | Manage DEB packages (Debian/Ubuntu) | `name`, `state` (present/absent/latest) |
| **pip** | Manage Python packages | `name`, `state` (present/absent/latest) |

### 📁 File Operations

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| **copy** | Copy files to remote systems | `src`, `dest`, `content` |
| **copyfrom** | Copy files from remote systems | `src`, `dest` |
| **lineinfile** | Modify specific lines in files | `path`, `line`, `regexp` |
| **template** | Process Jinja2 templates | `src`, `dest`, `variables` |
| **chmod** | Change file permissions | `path`, `mode` |
| **chown** | Change file ownership | `path`, `owner`, `group` |
| **mkdir** | Create directories | `path`, `mode` |
| **unarchive** | Extract archives | `src`, `dest` |

### 🌐 Network & Infrastructure

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| **get_url** | Download files from URLs | `url`, `dest` |
| **firewalld** | Manage firewall rules | `service`, `port`, `state` |
| **linode** | Manage Linode cloud instances | `name`, `type`, `region` |

### 🔐 Security & Access

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| **authorized_key** | Manage SSH public keys | `user`, `key`, `state` |
| **setsebool** | Configure SELinux booleans | `name`, `state` |
| **certbot** | Manage SSL certificates | `domains`, `email` |

### 🐳 Containers

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| **podman** | Manage Podman containers | `action` (pull/run/version), `image`, `name` |

### 💬 Communication

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| **slack** | Send Slack notifications | `channel`, `message`, `token` |
| **discord** | Send Discord notifications | `webhook_url`, `content` |

### ⚙️ Development Tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| **git** | Git repository operations | `repo`, `dest`, `version` |
| **bash** | Execute shell commands | `command` |
| **java_jar** | Manage Java JAR execution | `jar`, `args` |

### 🔧 System Services

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| **systemd_service** | Manage systemd services | `name`, `state`, `enabled` |
| **swapfile** | Configure swap files | `path`, `size` |

## Common Usage Patterns

### Basic Tool Usage

```python
import ftl_automation

with ftl_automation.automation(
    inventory="inventory.yml",
    tools=["hostname", "service", "dnf"]
) as ftl:
    # Set hostname
    ftl.hostname(name="webserver-01")
    
    # Install package
    ftl.dnf(name="nginx", state="present")
    
    # Start service
    ftl.service(name="nginx", state="started")
```

### File Management

```python
with ftl_automation.automation(
    inventory="inventory.yml", 
    tools=["copy", "lineinfile", "chmod"]
) as ftl:
    # Copy configuration file
    ftl.copy(
        src="nginx.conf",
        dest="/etc/nginx/nginx.conf"
    )
    
    # Modify configuration
    ftl.lineinfile(
        path="/etc/nginx/nginx.conf",
        line="worker_processes auto;",
        regexp="^worker_processes"
    )
    
    # Set permissions
    ftl.chmod(path="/etc/nginx/nginx.conf", mode="0644")
```

### User and Security Management

```python
with ftl_automation.automation(
    inventory="inventory.yml",
    tools=["user", "authorized_key", "firewalld"]
) as ftl:
    # Create user
    ftl.user(name="appuser", state="present", groups="wheel")
    
    # Add SSH key
    ftl.authorized_key(
        user="appuser",
        key="ssh-rsa AAAAB3NzaC1yc2E...",
        state="present"
    )
    
    # Configure firewall
    ftl.firewalld(service="ssh", state="enabled")
    ftl.firewalld(port="443/tcp", state="enabled")
```

### Container Operations

```python
with ftl_automation.automation(
    inventory="inventory.yml",
    tools=["podman"]
) as ftl:
    # Pull container image
    ftl.podman(action="pull", image="nginx:latest")
    
    # Run container
    ftl.podman(
        action="run",
        image="nginx:latest", 
        name="web-container"
    )
```

### Communication & Notifications

```python
with ftl_automation.automation(
    inventory="inventory.yml",
    tools=["slack", "discord"]
) as ftl:
    # Send Slack notification
    ftl.slack(
        channel="#deployments",
        message="Deployment completed successfully!",
        token="xoxb-your-token"
    )
    
    # Send Discord notification
    ftl.discord(
        webhook_url="https://discord.com/api/webhooks/...",
        content="Server maintenance completed"
    )
```

## Tool Implementation Details

### AutomationTool Base Class

All tools inherit from `AutomationTool` and follow this pattern:

```python
from ftl_automation import AutomationTool
import faster_than_light as ftl

class MyTool(AutomationTool):
    name = "my_tool"
    module = "my_module"
    description = "Description of what this tool does"
    
    def __call__(self, param1: str, param2: str = "default"):
        """Tool implementation with typed parameters"""
        # Execute FTL module
        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            self.module,
            # ... other parameters
            module_args=dict(param1=param1, param2=param2)
        )
        return output
```

### Context Access

Tools have access to the automation context:

- `self.context.inventory` - Target hosts and configuration
- `self.context.modules` - Available FTL modules  
- `self.context.console` - Rich console for output
- `self.context.secrets` - Secure credential storage

### Error Handling

Tools automatically handle common error scenarios:

- Module execution failures
- Network timeouts
- Permission errors
- Missing dependencies

Results are returned as dictionaries with standard fields:

```python
{
    "changed": True/False,
    "failed": True/False,
    "msg": "Status message",
    "rc": 0,  # Return code for commands
    "stdout": "Command output",
    "stderr": "Error output"
}
```

## Tool Development

### Creating New Tools

1. **Define the module** in FTL modules directory with YAML documentation
2. **Generate the tool** using the automated generator:
   ```bash
   python scripts/generate_tools.py --module my_module
   ```
3. **Review and customize** the generated tool code
4. **Update the __init__.py** to export the new tool
5. **Test the tool** in automation scripts

### Tool Generator

The tool generator creates standardized tool implementations from module documentation:

```bash
# Generate all tools
python scripts/generate_tools.py

# Generate specific tools
python scripts/generate_tools.py --module hostname --module service

# Use custom configuration
python scripts/generate_tools.py --simple-args-config custom_args.yaml
```

### Best Practices

1. **Keep tools simple** - One tool should do one thing well
2. **Use type hints** - Specify parameter types for better AI interaction
3. **Provide clear descriptions** - Include helpful docstrings
4. **Handle errors gracefully** - Return meaningful error messages
5. **Follow naming conventions** - Use descriptive, consistent names

## Advanced Usage

### Custom Tool Packages

Tools can be organized into custom packages:

```python
with ftl_automation.automation(
    tool_packages=["ftl_tools.tools", "my_custom_tools"],
    tools=["hostname", "my_custom_tool"]
) as ftl:
    ftl.hostname(name="server-01")
    ftl.my_custom_tool(param="value")
```

### Dynamic Tool Loading

Tools can be loaded dynamically from files:

```python
with ftl_automation.automation(
    tools_files=["custom_tools.py"],
    inventory="hosts.yml"
) as ftl:
    # Use tools defined in custom_tools.py
    ftl.custom_tool(param="value")
```

### Integration with AI Agents

Tools are designed for AI agent integration with clear interfaces:

```python
# Agent can discover available tools
available_tools = ftl.get_available_tools()

# Agent can get tool documentation  
tool_help = ftl.get_tool_help("hostname")

# Agent can execute tools with validation
result = ftl.hostname(name="validated-hostname")
```

## Troubleshooting

### Common Issues

1. **Module not found** - Ensure FTL modules are available in the modules path
2. **Permission denied** - Check SSH keys and user permissions
3. **Tool import errors** - Verify tool packages are installed
4. **Connection failures** - Check inventory configuration and network connectivity

### Debugging Tools

Enable verbose output for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

with ftl_automation.automation(inventory="hosts.yml") as ftl:
    # Debug output will show detailed execution
    result = ftl.hostname(name="debug-host")
```

## See Also

- [FTL Automation Documentation](../ftl-automation/README.md)
- [Tool Development Guide](TOOL_DEVELOPMENT.md)
- [Examples and Tutorials](../examples/)
- [API Reference](API_REFERENCE.md)
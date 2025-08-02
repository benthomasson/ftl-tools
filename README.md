
# FTL Tools

A library of infrastructure automation tools for FTL (Faster Than Light) agents. This library provides AI agents with standardized tool interfaces for managing remote systems, services, and deployments.

## Overview

ftl-tools wraps infrastructure automation modules (similar to Ansible modules) into a smolagents-compatible tool interface, enabling AI agents to perform DevOps and system administration tasks programmatically.

## Features

- **System Management**: Control services, users, packages, and system configuration
- **File Operations**: Edit files, manage permissions, copy files to/from remote systems  
- **Infrastructure**: Provision cloud servers, configure firewalls, manage SSL certificates
- **Container Management**: Podman operations for container deployment
- **Communication**: Send notifications via Slack/Discord
- **Security**: Manage SELinux settings, SSH keys, and access controls

## Installation

```bash
pip install -e .
```

## Tool Generation

The `generate_tools.py` script automatically creates tool wrapper classes from automation module documentation using AI code generation.

### Basic Usage

```bash
# Generate tools for all modules
python scripts/generate_tools.py

# Generate tools for specific modules
python scripts/generate_tools.py --module slack --module service

# Use custom directories
python scripts/generate_tools.py --modules-dir custom_modules --output-dir generated_tools
```

### Command Options

| Option | Default | Description |
|--------|---------|-------------|
| `--modules-dir` | `modules` | Directory containing module files to process |
| `--output-dir` | `tools` | Directory to save generated tool files |
| `--module` | (all) | Specific module(s) to generate (can be used multiple times) |
| `--model` | `claude-sonnet-4-20250514` | LLM model to use for code generation |
| `--simple-args-config` | (none) | JSON/YAML file with additional simple args configuration |

### Examples

```bash
# Generate tool for a single module
python scripts/generate_tools.py --module git

# Generate multiple specific tools
python scripts/generate_tools.py --module slack --module discord --module firewalld

# Use different AI model
python scripts/generate_tools.py --model gpt-4 --module service

# Custom configuration
python scripts/generate_tools.py \
  --modules-dir /path/to/modules \
  --output-dir /path/to/tools \
  --simple-args-config config.yaml \
  --module timezone --module hostname
```

### Supported Modules

The generator automatically processes modules with simple argument patterns:

- **Communication**: slack, discord
- **System Services**: service, systemd_service, hostname, timezone
- **Package Management**: dnf, apt, pip
- **File Management**: lineinfile, get_url, unarchive
- **Security**: authorized_key, firewalld, setsebool
- **Version Control**: git
- **Containers**: podman (pull, run, version)
- **SSL**: certbot
- **Templates**: template

### Custom Simple Args Configuration

Create a YAML or JSON file to define argument patterns for additional modules:

```yaml
# simple_args.yaml
my_custom_module:
  - param1
  - param2
  - optional_param

another_module:
  - required_arg
  - state
```

```bash
python scripts/generate_tools.py --simple-args-config simple_args.yaml --module my_custom_module
```

## Architecture

### Tool Pattern

All generated tools follow a consistent pattern:

```python
class ModuleName(Tool):
    name = "module_name_tool"
    module = "module_name"
    
    def __init__(self, state, *args, **kwargs):
        self.state = state  # Contains inventory, console, secrets, etc.
        
    def forward(self, param1: str, param2: str = "default") -> bool:
        display_tool(self, self.state["console"], self.state["log"])
        output = ftl.run_module_sync(...)
        display_results(output, self.state["console"], self.state["log"])
        return output
```

### State Management

Tools receive a `state` dictionary containing:
- `inventory`: Target systems/hosts configuration
- `console`: Rich console for formatted output
- `secrets`: Secure credential storage
- `gate_cache`, `gate`: FTL execution caching and gating
- `modules`: Available automation modules
- `workspace`: Working directory for file operations

## Development

### Requirements

- Python 3.8+
- litellm (for AI code generation)
- click (for CLI)
- rich (for output formatting)
- faster_than_light (FTL framework)
- smolagents (tool interface)

### Adding New Tools

1. Create or update automation module in `modules/` directory
2. Add module documentation in YAML format
3. Run the generator:
   ```bash
   python scripts/generate_tools.py --module your_module
   ```
4. Review and test the generated tool in `tools/` directory

### Customizing Generation

- **Template**: Edit `scripts/tool_template_prompt.txt` to modify the code generation template
- **Simple Args**: Add module patterns to the `SIMPLE_ARGS` dict in `generate_tools.py`
- **Model**: Use `--model` to try different AI models via LiteLLM

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

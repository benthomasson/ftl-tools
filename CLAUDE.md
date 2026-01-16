# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ftl-tools is a library that wraps infrastructure automation modules (similar to Ansible modules) into AI-compatible tool interfaces. It enables AI agents to perform DevOps and system administration tasks programmatically using the FTL (Faster Than Light) framework.

## Key Commands

### Installation and Setup
```bash
pip install -e .
```

### Tool Generation (Primary Development Workflow)
```bash
# Generate all tools from automation modules
python scripts/generate_tools.py

# Generate specific tools
python scripts/generate_tools.py --module hostname --module service

# Use custom AI model for generation
python scripts/generate_tools.py --model gpt-4 --module slack

# Use custom simple args configuration
python scripts/generate_tools.py --simple-args-config custom_args.yaml
```

### No Test Suite
This project does not include a traditional test suite. Functionality is validated through the tool generation process and manual testing with FTL automation scripts.

## Architecture

### Tool Generation System
- **AI-Generated Tools**: Tools are automatically generated from module documentation using LiteLLM and language models
- **Template-Based**: Uses `scripts/tool_template_prompt.txt` as the generation template
- **Configuration-Driven**: `scripts/simple_args.yaml` defines which module parameters to include in generated tools

### Tool Architecture Patterns

#### Current AutomationTool Pattern (ftl_tools/tools/)
```python
class ToolName(AutomationTool):
    name = "tool_name"
    module = "module_name"
    description = "Tool description"
    
    def __call__(self, param1: str, param2: str = "default"):
        display_tool(self, self.context.console, getattr(self.context, 'log', None))
        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            self.module,
            # ... context parameters
            module_args=dict(param1=param1, param2=param2)
        )
        display_results(output, self.context.console, getattr(self.context, 'log', None))
        return output
```

#### Legacy Async Tool Pattern (ftl_tools/async_tools.py)
```python
class ToolName(Tool):
    name = "tool_name"
    module = "module_name"
    
    def __init__(self, state, *args, **kwargs):
        self.state = state
        
    async def forward(self, param1: str, param2: str = "default") -> bool:
        # Async implementation using state dict
        display_tool(self, self.state['console'], self.state['log'])
        output = await ftl.run_module(...)
        display_results(output, self.state['console'], self.state['log'])
        return True
```

### Key Components

#### Context Management
- **AutomationContext**: New pattern providing structured access to inventory, modules, console, secrets
- **State Dictionary**: Legacy pattern with direct dict access to context elements

#### Module Integration  
- **FTL Modules**: Backend automation modules with YAML documentation
- **Dependencies**: Standard dependencies defined in `ftl_tools/utils.py:dependencies`
- **Module Execution**: Both sync (`ftl.run_module_sync`) and async (`ftl.run_module`) execution modes

#### Display System
- **Rich Console**: Formatted output using Rich library for tool execution feedback
- **Result Display**: Standardized success/failure/change reporting via `display_results()`
- **Tool Identification**: Tool execution logging via `display_tool()`

### Module Documentation Requirements
For a module to be auto-generated into a tool:
1. Must have YAML `DOCUMENTATION` constant with `module`, `short_description`, and `options` fields
2. Module name must be listed in `scripts/simple_args.yaml` with parameter subset
3. Module file must be in the `modules/` directory (configurable via `--modules-dir`)

### Tool Categories
- **System Administration**: hostname, service, user, timezone
- **Package Management**: dnf, apt, pip  
- **File Operations**: copy, copyfrom, lineinfile, template, chmod, chown, mkdir
- **Security**: authorized_key, setsebool, firewalld, certbot
- **Infrastructure**: linode (cloud provisioning), get_url
- **Containers**: podman operations
- **Communication**: slack, discord notifications
- **Version Control**: git operations

## Development Workflow

### Adding New Tools
1. Create/update automation module in `modules/` directory with YAML documentation
2. Add module parameters to `scripts/simple_args.yaml`
3. Run: `python scripts/generate_tools.py --module your_module`
4. Review generated tool in `ftl_tools/tools/your_module.py`
5. Update `ftl_tools/tools/__init__.py` to export new tool
6. Test tool in automation context

### Customizing Tool Generation
- **Template Modification**: Edit `scripts/tool_template_prompt.txt` to change generated code patterns
- **Model Selection**: Use `--model` flag to specify different AI models via LiteLLM
- **Parameter Configuration**: Modify `scripts/simple_args.yaml` or provide custom config file

### Migration Considerations
The codebase shows signs of migration from async Tool pattern to sync AutomationTool pattern. When working on tools:
- Prefer the AutomationTool pattern for new tools (ftl_tools/tools/)
- Legacy async tools remain in async_tools.py but aren't actively generated
- New tools use `self.context` instead of `self.state` dict
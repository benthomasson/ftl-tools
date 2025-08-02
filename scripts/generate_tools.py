#!/usr/bin/env python3

"""
Extract the documentation from a module and generate a tool interface for it.
"""

import yaml
from rich import print
import litellm
import ast
import re
import glob
import os
import importlib
import click


# based on smolagents/src/smolagents/util.py
def parse_code_blobs(code_blob: str) -> str:
    """Parses the LLM's output to get any code blob inside. Will return the
    code directly if it's code."""
    pattern = r"```(?:py|python)?\n(.*?)\n```"
    matches = re.findall(pattern, code_blob, re.DOTALL)
    if len(matches) == 0:
        try:  # Maybe the LLM outputted a code blob directly
            ast.parse(code_blob)
            return code_blob
        except SyntaxError:
            pass
        return None
    return "\n\n".join(match.strip() for match in matches)


def load_simple_args_config(simple_args_config):
    """Load simple args configuration from default and optional config files"""
    # Load default simple args configuration
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_config_path = os.path.join(script_dir, 'simple_args.yaml')
    
    with open(default_config_path, 'r') as f:
        simple_args = yaml.safe_load(f)

    # Load additional simple args configuration from file if provided
    if simple_args_config:
        import json
        with open(simple_args_config, 'r') as f:
            if simple_args_config.endswith('.json'):
                simple_args.update(json.load(f))
            else:
                simple_args.update(yaml.safe_load(f))
    
    return simple_args


def get_module_paths(modules_dir, module_names):
    """Get list of module paths to process based on specified modules or all modules"""
    if module_names:
        # Process only specified modules
        module_paths = []
        for mod_name in module_names:
            mod_path = f"{modules_dir}/{mod_name}.py"
            if os.path.exists(mod_path):
                module_paths.append(mod_path)
            else:
                print(f"Warning: Module file {mod_path} not found")
    else:
        # Process all modules in directory
        module_paths = glob.glob(f"{modules_dir}/*.py")
    
    return module_paths


def should_skip_module(module_name, output_dir):
    """Check if module should be skipped"""
    # Skip if tool already exists
    if os.path.exists(f"{output_dir}/{module_name}.py"):
        return True
    
    # Skip system modules
    if module_name in ["command", "__init__"]:
        return True
    
    return False


def load_module(module_path):
    """Load a Python module from file path"""
    module_name = os.path.splitext(os.path.basename(module_path))[0]

    # Load module from file path
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def extract_module_docs(module):
    """Extract YAML documentation from module"""
    try:
        return yaml.safe_load(module.DOCUMENTATION)
    except AttributeError:
        return None


def build_options_for_module(module_name, docs, simple_args):
    """Build options dict for module based on simple args configuration"""
    if module_name not in simple_args:
        return None
    
    options = {}
    for option in simple_args[module_name]:
        options[option] = docs["options"][option]
    
    return options


def build_module_documentation(docs, options):
    """Build documentation string for LLM prompt"""
    doc = f"""
    # {docs["module"]} module

    ## Description
    {docs["short_description"]}

    ## Options
    """

    for option in options:
        doc += "* {option}: {type} {help}".format(
            option=option,
            type=options[option]["type"],
            help=options[option]["description"][0].split(". ")[0],
        )
        if default := options[option].get('default'):
            doc += f" default = {default}\n"
        else:
            doc += "\n"
    
    return doc


def load_system_prompt():
    """Load system prompt from external file"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, 'tool_template_prompt.txt'), 'r') as f:
        return f.read()


def generate_tool_code(doc, model, system_prompt):
    """Generate tool code using LLM"""
    prompt = f"""Using this documentation for a automation module
    generate a tool interface.
    {doc}
    """

    print(system_prompt)
    print(prompt)

    # Call the model
    response = litellm.completion(
        model=model,
        messages=[
            {
                "role": "system", 
                "content": system_prompt,
                "cache_control": {"type": "ephemeral"}
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )

    return response["choices"][0]["message"]["content"]


def save_generated_code(generated_code, output_path):
    """Save generated code to file after validation"""
    code = parse_code_blobs(generated_code)
    print("=" * 80)
    print(f"Extracted code: {code}")
    print("=" * 80)
    
    if not code:
        return False
    
    try:
        ast.parse(code)
    except SyntaxError as e:
        print(f"Failed with syntax error: {e}")
        return False

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"✅ Code saved to {output_path}")
    return True


def process_module(module_path, simple_args, model, output_dir, system_prompt):
    """Process a single module and generate tool code"""
    module_name = os.path.splitext(os.path.basename(module_path))[0]

    if should_skip_module(module_name, output_dir):
        return False

    try:
        module = load_module(module_path)
        print(f"Processing module: {module}")
    except BaseException as e:
        print(f"Failed to load {module_path}: {e}")
        return False

    docs = extract_module_docs(module)
    if not docs:
        print(f"No documentation found in {module_path}")
        return False

    print(f"Found module: {docs['module']}")

    options = build_options_for_module(module_name, docs, simple_args)
    if not options:
        print(f"Module {module_name} not in simple args configuration")
        return False

    print(f"Module options: {options}")

    doc = build_module_documentation(docs, options)
    print(doc)

    generated_code = generate_tool_code(doc, model, system_prompt)
    print(generated_code)

    output_path = f"{output_dir}/{module_name}.py"
    return save_generated_code(generated_code, output_path)

@click.command()
@click.option('--modules-dir', default='modules', help='Directory containing module files to process')
@click.option('--simple-args-config', type=click.Path(exists=True), help='JSON/YAML file containing simple args configuration')
@click.option('--model', default='claude-sonnet-4-20250514', help='LLM model to use for code generation')
@click.option('--output-dir', default='tools', help='Directory to save generated tool files')
@click.option('--module', multiple=True, help='Specific module(s) to generate (can be used multiple times)')
def main(modules_dir, simple_args_config, model, output_dir, module):
    """Generate tool wrappers from module documentation using AI"""
    
    # Load configuration
    simple_args = load_simple_args_config(simple_args_config)
    system_prompt = load_system_prompt()
    
    # Get modules to process
    module_paths = get_module_paths(modules_dir, module)
    
    # Process each module
    success_count = 0
    total_count = len(module_paths)
    
    for module_path in module_paths:
        if process_module(module_path, simple_args, model, output_dir, system_prompt):
            success_count += 1
    
    print(f"\n✅ Successfully generated {success_count}/{total_count} tools")

if __name__ == "__main__":
    main()

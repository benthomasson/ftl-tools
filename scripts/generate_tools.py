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


def load_module(module_path):

    module_name = os.path.splitext(os.path.basename(module_path))[0]

    # Load module from file path
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module

@click.command()
@click.option('--modules-dir', default='modules', help='Directory containing module files to process')
@click.option('--simple-args-config', type=click.Path(exists=True), help='JSON/YAML file containing simple args configuration')
@click.option('--model', default='claude-sonnet-4-20250514', help='LLM model to use for code generation')
@click.option('--output-dir', default='tools', help='Directory to save generated tool files')
def main(modules_dir, simple_args_config, model, output_dir):

    SIMPLE_ARGS = {
        "slack": ["token", "msg"],
        "service": ["name", "state"],
        "lineinfile": ["line", "state", "path", "regexp"],
        "authorized_key": ["user", "state", "key"],
        "user": ["name", "group"],
        "dnf": ["name", "state"],
        "apt": ["update_cache", "upgrade"],
        "hostname": ["name"],
        "discord": ["content"],
        "firewalld": ["port", "state", "permanent"],
        "unarchive": ["src", "dest"],
        "pip": ["name", "state"],
        "get_url": ["url", "dest"],
        "systemd_service": ["name", "state", "enabled"],
        "timezone": ["name"],
        "git": ["repo", "dest", "update"],
    }

    # Load simple args configuration from file if provided
    if simple_args_config:
        import json
        with open(simple_args_config, 'r') as f:
            if simple_args_config.endswith('.json'):
                SIMPLE_ARGS.update(json.load(f))
            else:
                SIMPLE_ARGS.update(yaml.safe_load(f))

    for module_path in glob.glob(f"{modules_dir}/*.py"):

        module_name = os.path.splitext(os.path.basename(module_path))[0]

        if os.path.exists(f"{output_dir}/{module_name}.py"):
            continue

        if module_name in ["command", "__init__"]:
            continue

        try:
            module = load_module(module_path)
            print(module)
        except BaseException as e:
            print(module_path, e)
            continue

        try:
            docs = yaml.safe_load(module.DOCUMENTATION)
        except AttributeError:
            continue
        # print(docs.keys())
        print(docs["module"])
        # print(docs['description'])
        # print(docs['short_description'])
        # print(docs['options'].keys())

        # simple_options = ["token", "msg"]

        if module_name in SIMPLE_ARGS:
            options = {}
            for option in SIMPLE_ARGS[module_name]:
                options[option] = docs["options"][option]
            print(options)
        else:
            continue
            # options = docs["options"]

        doc = """
        # {module} module

        ## Description
        {short_description}

        ## Options
        """.format(
            module=docs["module"], short_description=docs["short_description"]
        )

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

        print(doc)

        system_prompt = """You are a helpful code assistant. Use the following
        template to make tool interfaces from modules:


        ```python
        from smolagents.tools import Tool
        from ftlagents.tools import get_json_schema
        import faster_than_light as ftl
        from ftl_tools.utils import dependencies, display_results, display_tool


        class ModuleName(Tool):
            name = "module_name_tool"
            module = "module_name"

            def __init__(self, state, *args, **kwargs):
                self.state = state
                super().__init__(*args, **kwargs)

            def forward(self, arg1: str, arg2: str) -> bool:
                '''Module description

                Args:
                    arg1: argument 1 description
                    arg2: argument 2 description

                Returns:
                    boolean
                '''
                display_tool(self, self.state["console"], self.state["log"])

                output = ftl.run_module_sync(
                    self.state["inventory"],
                    self.state["modules"],
                    self.module,
                    self.state["gate_cache"],
                    module_args=dict(arg1=arg1, arg2=arg2),
                    dependencies=dependencies,
                    loop=self.state["loop"],
                    use_gate=self.state["gate"],
                )

                display_results(output, self.state["console"], self.state["log"])

                return output

            description, inputs, output_type = get_json_schema(forward)
        ```


        For the return value choose one of: string, boolean, integer, number, object, any, or null.
        Do not include a description for the return value.

        If the default is included for an argument, add the default to the forward function arguments.


        """

        prompt = f"""Using this documentation for a automation module
        generate a tool interface.
        {doc}
        """

        print(system_prompt)
        print(prompt)

        max_tokens = 3000
        temperature = 0.0
        output = f"{output_dir}/{module_name}.py"

        done = False
        while not done:
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
                #max_tokens=max_tokens,
                temperature=temperature,
                #num_ctx=8192,
                #api_base="http://host.docker.internal:11434"
            )

            generated_code = response["choices"][0]["message"]["content"]
            print(generated_code)
            code = parse_code_blobs(generated_code)
            print("=" * 80)
            print(f"{code=}")
            print("=" * 80)
            if not code:
                continue
            try:
                ast.parse(code)
            except SyntaxError as e:
                print("Failed with syntax error", e)
                continue

            if output:
                # Ensure output directory exists
                os.makedirs(output_dir, exist_ok=True)
                with open(output, "w", encoding="utf-8") as f:
                    f.write(code)
                print(f"✅ Code saved to {output}")
                done = True
            else:
                print("Generated Code:\n")
                print(code)
                done = True

if __name__ == "__main__":
    main()

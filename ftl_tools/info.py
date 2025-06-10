

import inspect

import ftl_tools
from smolagents.tools import Tool
from ftlagents.tools import get_json_schema


if __name__ == "__main__":

    print("Tools")
    for name, obj in inspect.getmembers(ftl_tools):
        if inspect.isclass(obj):
            if obj == Tool:
                continue
            tool = obj
            description, inputs, output_type = get_json_schema(tool.forward)
            print(f"* {tool.name} - {description}")

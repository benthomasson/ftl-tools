
import json

from rich.pretty import pprint
from rich.rule import Rule


dependencies = [
    "ftl_module_utils @ git+https://github.com/benthomasson/ftl_module_utils@main",
    "ftl_collections @ git+https://github.com/benthomasson/ftl-collections@main",
]


def write_or_print(output, console, log):

    if log is None:
        console.print(output)
    else:
        log.write(output)


def display_tool(tool, console, log):
    write_or_print(
        Rule(title=f"\n[green]TOOL [white]\[{tool.name}]", align="left"),  # noqa: W605
        console,
        log,
    )


def display_results(output, console, log):
    if log is None:
        pprint(output, console=console)
        for name, results in output.items():
            if results.get("failed"):
                raise Exception(results.get("msg"))
            if results.get("changed"):
                console.print(f"[yellow] changed: [{name}]")
            else:
                console.print(f"[green] ok: [{name}]")
        console.print("")
        console.print_json(json.dumps(output))
    else:
        log.write(output)
        for name, results in output.items():
            if results.get("failed"):
                raise Exception(results.get("msg"))
            if results.get("changed"):
                log.write(f"[yellow] changed: [{name}]")
            else:
                log.write(f"[green] ok: [{name}]")
        log.write("")
        log.write(json.dumps(output))

#!/usr/bin/env python3
from smolagents.tools import Tool
from ftlagents.tools import get_json_schema

import yaml
from linode_api4 import LinodeClient
from rich.pretty import pprint
from ftl_automation_agent import console

from ftl_tools.utils import display_results, display_tool


class Linode(Tool):
    name = "linode_tool"
    module = None

    def __init__(self, state, *args, **kwargs):
        self.state = state
        super().__init__(*args, **kwargs)

    def forward(
        self, name: str, image: str = "linode/fedora40", ltype: str = "g6-nanode-1"
    ) -> bool:
        """Provisions a new linode server

        Args:
            name: the name of the server
            image: the name of the server image to use
            ltype: the linode type of the server

        Returns:
            boolean
        """
        display_tool(self, self.state["console"], self.state["log"])

        pprint(self.state["inventory"], console=console)

        # Create a Linode API client
        client = LinodeClient(str(self.state["secrets"]["LINODE_TOKEN"]))
        root_pass = self.state["secrets"]["LINODE_ROOT_PASS"]

        my_linodes = client.linode.instances()

        for instance in my_linodes:
            if instance.label == name:
                console.print(f"Already created {name}")
                return True

        # Create a new Linode
        new_linode = client.linode.instance_create(
            ltype=ltype,
            region="us-southeast",
            image=image,
            label=name,
            root_pass=str(root_pass),
            authorized_users=["benthomasson"],
        )

        # Print info about the Linode
        console.print("Linode IP:", new_linode.ipv4[0])

        host_data = {
            "ansible_user": "root",
            "ansible_host": new_linode.ipv4[0],
            "ansible_python_interpreter": "/usr/bin/python3",
            "host_name": name,
        }
        if self.state["inventory"].get("all") is None:
            self.state["inventory"]["all"] = {}
        if self.state["inventory"]["all"].get("hosts") is None:
            self.state["inventory"]["all"]["hosts"] = {}
        self.state["inventory"]["all"]["hosts"][name] = host_data

        with open(self.state["inventory_file"], "w") as f:
            f.write(yaml.safe_dump(self.state["inventory"]))

        pprint(self.state["inventory"], console=console)

        return {"localhost": {"changed": True}}

    description, inputs, output_type = get_json_schema(forward)
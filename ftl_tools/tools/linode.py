#!/usr/bin/env python3
import yaml
from linode_api4 import LinodeClient
from rich.pretty import pprint

from ftl_automation import AutomationTool
from ftl_tools.utils import display_results, display_tool


class Linode(AutomationTool):
    name = "linode"
    module = None  # This tool doesn't use FTL modules, it uses Linode API directly
    description = "Provisions a new linode server"

    def __call__(self, name: str, image: str = "linode/fedora40", ltype: str = "g6-nanode-1"):
        """Provisions a new linode server

        Args:
            name: the name of the server
            image: the name of the server image to use
            ltype: the linode type of the server

        Returns:
            Server provisioning result
        """
        display_tool(self, self.context.console, getattr(self.context, 'log', None))

        pprint(self.context.inventory, console=self.context.console)

        # Create a Linode API client
        client = LinodeClient(str(self.context.secrets["LINODE_TOKEN"]))
        root_pass = self.context.secrets["LINODE_ROOT_PASS"]

        my_linodes = client.linode.instances()

        for instance in my_linodes:
            if instance.label == name:
                self.context.console.print(f"Already created {name}")
                return {
                    "id": instance.id,
                    "label": instance.label,
                    "image": image,
                    "type": ltype,
                    "status": instance.status,
                    "ipv4": instance.ipv4,
                    "ipv6": instance.ipv6
                }

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
        self.context.console.print("Linode IP:", new_linode.ipv4[0])

        host_data = {
            "ansible_user": "root",
            "ansible_host": new_linode.ipv4[0],
            "ansible_python_interpreter": "/usr/bin/python3",
            "host_name": name,
        }
        
        if self.context.inventory.get("all") is None:
            self.context.inventory["all"] = {}
        if self.context.inventory["all"].get("hosts") is None:
            self.context.inventory["all"]["hosts"] = {}
        self.context.inventory["all"]["hosts"][name] = host_data

        # Save inventory if file path provided
        if self.context.inventory_file:
            with open(self.context.inventory_file, "w") as f:
                f.write(yaml.safe_dump(self.context.inventory))

        pprint(self.context.inventory, console=self.context.console)

        return {
            "id": new_linode.id,
            "label": new_linode.label,
            "image": image,
            "type": ltype,
            "status": new_linode.status,
            "ipv4": new_linode.ipv4,
            "ipv6": new_linode.ipv6
        }
#!/usr/bin/env python3
import yaml
from linode_api4 import LinodeClient
from rich.pretty import pprint

from ftl_tools.base_tool import AutomationTool
from ftl_tools.utils import display_results, display_tool


class Linode(AutomationTool):
    name = "linode_tool"
    module = None
    description = "Provisions a new linode server"

    def __init__(self, inventory, modules, console, secrets=None, **kwargs):
        super().__init__(inventory, modules, console, secrets, **kwargs)
        # Build state dictionary for compatibility
        self.state = {
            "inventory": inventory,
            "modules": modules,
            "console": console,
            "secrets": secrets or {},
            **kwargs
        }

    def forward(self, name: str, image: str = "linode/fedora40", ltype: str = "g6-nanode-1"):
        """Provisions a new linode server

        Args:
            name: the name of the server
            image: the name of the server image to use
            ltype: the linode type of the server

        Returns:
            Server provisioning result
        """
        display_tool(self, self.state["console"], self.state.get("log"))

        pprint(self.state["inventory"], console=self.state["console"])

        # Create a Linode API client
        client = LinodeClient(str(self.state["secrets"]["LINODE_TOKEN"]))
        root_pass = self.state["secrets"]["LINODE_ROOT_PASS"]

        my_linodes = client.linode.instances()

        for instance in my_linodes:
            if instance.label == name:
                self.state["console"].print(f"Already created {name}")
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
        self.state["console"].print("Linode IP:", new_linode.ipv4[0])

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

        # Save inventory if file path provided
        if self.state.get("inventory_file"):
            with open(self.state["inventory_file"], "w") as f:
                f.write(yaml.safe_dump(self.state["inventory"]))

        pprint(self.state["inventory"], console=self.state["console"])

        return {
            "id": new_linode.id,
            "label": new_linode.label,
            "image": image,
            "type": ltype,
            "status": new_linode.status,
            "ipv4": new_linode.ipv4,
            "ipv6": new_linode.ipv6
        }


# Create function interface for ftl-automation  
def linode_tool(inventory, modules, console, name: str, 
                image: str = "linode/fedora40", ltype: str = "g6-nanode-1", **kwargs):
    """Provisions a new linode server.
    
    Args:
        inventory: Target systems/hosts configuration
        modules: Available automation modules
        console: Rich console for formatted output
        name: the name of the server
        image: the name of the server image to use
        ltype: the linode type of the server
        **kwargs: Additional context including secrets
        
    Returns:
        Server provisioning result
    """
    tool = Linode(inventory, modules, console, **kwargs)
    return tool(name=name, image=image, ltype=ltype)
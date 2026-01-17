#!/usr/bin/env python3
import os
import faster_than_light as ftl

from ftl_automation import AutomationTool
from ftl_tools.utils import dependencies, display_results, display_tool


class AuthorizedKey(AutomationTool):
    name = "authorized_key"
    module = "authorized_key"
    description = "Manage authorized keys and upload public keys to the remote node"

    def __call__(self, user: str, key_file: str, state: str = "present"):
        """Manage authorized keys and upload public keys to the remote node

        Args:
            user: the name of the user
            state: one of present or absent
            key_file: the path to the file containing the public key

        Returns:
            Module execution result
        """
        display_tool(self, self.context.console, getattr(self.context, 'log', None))
        
        key_file = os.path.abspath(os.path.expanduser(key_file))
        if not os.path.exists(key_file) or not os.path.isfile(key_file):
            raise Exception(f"{key_file} does not exist")
        
        with open(key_file) as f:
            key_value = f.read()
            
        # Prepare module args for authorized_key operation
        auth_key_module_args = dict(user=user, state=state, key=key_value)
        
        # Add check_mode if in dry run
        if getattr(self.context, 'dry_run', False):
            auth_key_module_args['_ansible_check_mode'] = True

        output = ftl.run_module_sync(
            self.context.inventory,
            self.context.modules,
            "authorized_key",
            getattr(self.context, 'gate_cache', None),
            module_args=auth_key_module_args,
            dependencies=dependencies,
            loop=getattr(self.context, 'loop', None),
            use_gate=getattr(self.context, 'use_gate', False),
        )

        display_results(output, self.context.console, getattr(self.context, 'log', None))

        return output

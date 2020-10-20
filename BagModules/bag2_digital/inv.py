# -*- coding: utf-8 -*-

from typing import Mapping, Any

import os
import pkg_resources

from bag.design.module import Module


# noinspection PyPep8Naming
class bag2_digital__inv(Module):
    """Module for library bag2_digital cell inv.

    Fill in high level description here.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'inv.yaml'))


    def __init__(self, database, parent=None, prj=None, **kwargs):
        Module.__init__(self, database, self.yaml_file, parent=parent, prj=prj, **kwargs)

    @classmethod
    def get_params_info(cls):
        # type: () -> Dict[str, str]
        """Returns a dictionary from parameter names to descriptions.

        Returns
        -------
        param_info : Optional[Dict[str, str]]
            dictionary from parameter names to descriptions.
        """
        return dict(
            seg_n = 'NMOS number of fingers',
            seg_p = 'PMOS number of fingers',
            w_n = 'NMOS width',
            w_p = 'PMOS width',
            th_n = 'NMOS threshold flavor',
            th_p = 'PMOS threshold flavor',
            lch = 'Channel length',
            stack_n = 'NMOS stack height',
            stack_p = 'PMOS stack height',
        )

    def design(self, **params):
        """To be overridden by subclasses to design this module.

        This method should fill in values for all parameters in
        self.parameters.  To design instances of this module, you can
        call their design() method or any other ways you coded.

        To modify schematic structure, call:

        rename_pin()
        delete_instance()
        replace_instance_master()
        reconnect_instance_terminal()
        restore_instance()
        array_instance()
        """
        # Design instances
        self.instances['XN'].design(
            lch = params['lch'],
            w = params['w_n'],
            stack = params['stack_n'],
            intent = params['th_n'],
            seg = params['seg_n'],
            export_mid = False)

        self.instances['XP'].design(
            lch = params['lch'],
            w = params['w_p'],
            stack = params['stack_p'],
            intent = params['th_p'],
            seg = params['seg_p'],
            export_mid = False)

        # Rewire as necessary
        stack_n = params['stack_n']
        stack_p = params['stack_p']

        if stack_p > 1:
            suffix_p = f"<{stack_p-1}:0>"
            suffix_gp = f'<{stack_p-2}:0>' if stack_p > 2 else ''
            g_p = f'VP{suffix_gp},in'
            self.add_pin(f'VP{suffix_gp}', 'input')
            self.reconnect_instance_terminal('XP', f'G{suffix_p}', g_p)

        if stack_n > 1:
            suffix_n = f"<{stack_n-1}:0>"
            suffix_gn = f'<{stack_n-2}:0>' if stack_n > 2 else ''
            g_n = f'VN{suffix_gn},in'
            self.add_pin(f'VN{suffix_gn}', 'input')
            self.reconnect_instance_terminal('XN', f'G{suffix_n}', g_n)
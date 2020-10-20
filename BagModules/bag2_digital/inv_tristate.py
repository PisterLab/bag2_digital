# -*- coding: utf-8 -*-

from typing import Dict

import os
import pkg_resources

from bag.design.module import Module


# noinspection PyPep8Naming
class bag2_digital__inv_tristate(Module):
    """Module for library bag2_digital cell inv_tristate.

    Tristate inverter with variable sizing between devices.
    uses bag2_analog/nmos4_astack and pmos4_astack.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'inv_tristate.yaml'))


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
            nstack_params = 'NMOS analog stack parameters',
            pstack_params = 'PMOS analog stack parameters'
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
        nstack_params = params['nstack_params']
        pstack_params = params['pstack_params']

        # Design instances
        self.instances['XN'].design(**nstack_params)
        self.instances['XP'].design(**pstack_params)
        
        # Rewire/change pins as necessary
        stack_n = nstack_params['stack']
        stack_p = pstack_params['stack']

        assert stack_p > 1, f'P stack height {stack_p} should be > 1'
        assert stack_n > 1, f'N stack height {stack_n} should be > 1'

        pin_vn = 'VN'
        if stack_n > 2:
            pin_vn = f'VN<{stack_n-2}:0>'
            self.rename_pin('VN', pin_vn)
        if stack_n > 1:
            self.reconnect_instance_terminal('XN', f'G<{stack_n-1}:0>', pin_vn+',in')

        pin_vp = 'VP'
        if stack_p > 2:
            pin_vp = f'VP<{stack_p-2}:0>'
            self.rename_pin('VP', pin_vp)
        if stack_p > 1:            
            self.reconnect_instance_terminal('XP', f'G<{stack_p-1}:0>', pin_vp+',in')

        
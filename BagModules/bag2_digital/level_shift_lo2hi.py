# -*- coding: utf-8 -*-

from typing import Dict, Mapping

import os
import pkg_resources

from bag.design.module import Module


# noinspection PyPep8Naming
class bag2_digital__level_shift_lo2hi(Module):
    """Module for library bag2_digital cell level_shift_lo2hi.

    Fill in high level description here.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'level_shift_lo2hi.yaml'))


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
            inv_params = 'Low-voltage inverter parameters',
            n_params = 'NMOS parameters',
            p_params = 'High-voltage PMOS parameters'
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
        inv_params = params['inv_params']
        n_params = params['n_params']
        p_params = params['p_params']

        self.instances['XINV0'].design(stack_n=1, stack_p=1, **inv_params)
        self.instances['XINV1'].design(stack_n=1, stack_p=1, **inv_params)
        self.instances['XN0'].design(**n_params)
        self.instances['XN1'].design(**n_params)
        self.instances['XP0'].design(**p_params)
        self.instances['XP1'].design(**p_params)
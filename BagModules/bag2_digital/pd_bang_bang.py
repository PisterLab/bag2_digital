# -*- coding: utf-8 -*-

from typing import Dict

import os
import pkg_resources

from bag.design.module import Module


# noinspection PyPep8Naming
class bag2_digital__pd_bang_bang(Module):
    """Module for library bag2_digital cell pd_bang_bang.

    Fill in high level description here.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'pd_bang_bang.yaml'))


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
            dff_params='flipflop parameters',
            latch_params='Latch parameters',
            xor_params='XOR parameters'
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
        dff_params = params['dff_params']
        latch_params = params['latch_params']
        xor_params = params['xor_params']

        for i in range(2):
            self.instances[f'XDFF_IN<{i}>'].design(**dff_params)
        self.instances['XDFF_OUT<0>'].design(**dff_params)
        self.instances['XLATCH'].design(**latch_params)

        self.instances['XOR_T'].design(**xor_params)
        self.instances['XOR_E'].design(**xor_params)
# -*- coding: utf-8 -*-

from typing import Dict

import os
import pkg_resources

from bag.design.module import Module


# noinspection PyPep8Naming
class bag2_digital__mux2(Module):
    """Module for library bag2_digital cell mux2.

    Fill in high level description here.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'mux2.yaml'))


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
            inv_params='Inverter parameters for the select signal.',
            nand_in_params='NAND parameters for the direct input connections.',
            nand_out_params='NAND parameters for the output gate'
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
        inv_params      = params['inv_params']
        nand_in_params  = params['nand_in_params']
        nand_out_params = params['nand_out_params']

        self.instances['XINV'].design(**inv_params, stack_n=1, stack_p=1)
        self.instances['XNAND_IN<0>'].design(**nand_in_params, num_in=2)
        self.instances['XNAND_IN<1>'].design(**nand_in_params, num_in=2)
        self.instances['XNAND_OUT'].design(**nand_out_params, num_in=2)
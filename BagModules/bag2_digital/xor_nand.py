# -*- coding: utf-8 -*-

from typing import Dict, Mapping

import os
import pkg_resources

from bag.design.module import Module


# noinspection PyPep8Naming
class bag2_digital__xor_nand(Module):
    """Module for library bag2_digital cell xor_nand.

    Fill in high level description here.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'xor_nand.yaml'))


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
            nand_in_params='Parameters for the input NAND',
            nand_mid_params='Parameters for the intermediate NANDs',
            nand_out_params='Parameters for the output NAND'
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
        nand_in_params  = params['nand_in_params']
        nand_mid_params = params['nand_mid_params']
        nand_out_params = params['nand_out_params']
        
        self.instances['XNAND_IN'].design(**nand_in_params, num_in=2)
        self.instances['XNAND_MID<0>'].design(**nand_mid_params, num_in=2)
        self.instances['XNAND_MID<1>'].design(**nand_mid_params, num_in=2)
        self.instances['XNAND_OUT'].design(**nand_out_params, num_in=2)
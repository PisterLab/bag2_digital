# -*- coding: utf-8 -*-

from typing import Dict, Mapping

import os
import pkg_resources

from bag.design.module import Module


# noinspection PyPep8Naming
class bag2_digital__latch_SbRb(Module):
    """Module for library bag2_digital cell latch_SbRb.

    Fill in high level description here.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'latch_SbRb.yaml'))


    def __init__(self, database, parent=None, prj=None, **kwargs):
        Module.__init__(self, database, self.yaml_file, parent=parent, prj=prj, **kwargs)

    @classmethod
    def get_params_info(cls) -> Mapping[str,str]:
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
        nand_params = params.copy()
        nand_params.update(num_in=2)

        self.instances['XNANDSb'].design(**nand_params)
        self.instances['XNANDRb'].design(**nand_params)

        self.reconnect_instance_terminal('XNANDSb', 'in<1:0>', 'Sb,Qb')
        self.reconnect_instance_terminal('XNANDRb', 'in<1:0>', 'Rb,Q')

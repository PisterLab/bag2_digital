# -*- coding: utf-8 -*-

from typing import Dict, Mapping

import os
import pkg_resources
import warnings

from bag.design.module import Module


# noinspection PyPep8Naming
class bag2_digital__clkgen_nonoverlap(Module):
    """Module for library bag2_digital cell clkgen_nonoverlap.

    Fill in high level description here.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'clkgen_nonoverlap.yaml'))


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
            clk_inv_params = 'Initial clock inverter parameters',
            clk_sw_params = 'Initial transmission gate parameters',
            nand_params = 'Feedback NAND parameters',
            buf_params = 'Output buffer parameters which determine delay',
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
        clk_inv_params = params['clk_inv_params']
        clk_sw_params = params['clk_sw_params']
        nand_params = params['nand_params']
        buf_params = params['buf_params']

        ### ASSUMPTIONS ###
        # Switch is a transmission gate
        # NANDs have 2 inputs
        # Buffers must have an odd number of inverters
        # All inverter stacks are 1
        ###################

        buf_inv_list = buf_params['inv_param_list']
        assert len(buf_inv_list)%2==1, f'Must have an odd number of inverters in the buffer'
        assert len(buf_inv_list) > 2, f'Must have at least two inverters in the buffer'

        for inv in buf_inv_list:
            if inv.get('stack_n', 0) != 1 or inv.get('stack_p', 0) != 1:
                warnings.warn('(clkgen_nonoverlap) Changing all stacks to 1')
                inv.update(dict(stack_n=1, stack_p=1))

        self.instances['XINV_IN'].design(stack_n=1, stack_p=1, **clk_inv_params)
        self.instances['XSW_IN'].design(mos_type='both', **clk_sw_params)
        self.instances['XNANDA'].design(num_in=2, **nand_params)
        self.instances['XNANDB'].design(num_in=2, **nand_params)
        self.instances['XBUFA'].design(dual_output=True, **buf_params)
        self.instances['XBUFB'].design(dual_output=True, **buf_params)
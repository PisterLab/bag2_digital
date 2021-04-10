# -*- coding: utf-8 -*-

from typing import Dict, Mapping

import os
import pkg_resources

from bag.design.module import Module


# noinspection PyPep8Naming
class bag2_digital__flipflop_D_inv(Module):
    """Module for library bag2_digital cell flipflop_D_inv.

    Fill in high level description here.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'flipflop_D_inv.yaml'))


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
            tgate_params_list = 'List of parameters for each transmission gate. Master0 and 1, then slave 0 and 1',
            inv_params_list = 'List of parameters for each inverter. master0 and 1, then slave 0 and 1.',
            buf_params_list = 'List of inverter parameters for the clock buffer.'
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
        tgate_params_list = params['tgate_params_list']
        inv_params_list = params['inv_params_list']
        buf_params_list = params['buf_params_list']

        assert len(tgate_params_list) == 4, f'There are 4 transmission gates, not {len(tgate_params_list)}'
        assert len(inv_params_list) == 4, f'There are 4 inverters, not {len(inv_params_list)}'
        assert len(buf_params_list) > 1, f'Must have at least 2 inverters in clock buffer (currently {len(buf_params_list)})'

        idx_inst_map = ['M<0>', 'M<1>', 'S<0>', 'S<1>']

        for i, suffix in enumerate(idx_inst_map):
            self.instances[f'XTG_{suffix}'].design(mos_type='both', **(tgate_params_list[i]))
            self.instances[f'XINV_{suffix}'].design(stack_n=1, stack_p=1, **(inv_params_list[i]))

        for buf_params in buf_params_list:
            assert buf_params['stack_n'] == 1, f'Clock buffers should not be stacked'
            assert buf_params['stack_p'] == 1, f'Clock buffers should not be stacked'

        self.instances['XBUF'].design(dual_output=True, inv_param_list=buf_params_list)
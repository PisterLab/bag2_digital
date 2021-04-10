# -*- coding: utf-8 -*-

from typing import Dict, Mapping

import os
import pkg_resources

from bag.design.module import Module


# noinspection PyPep8Naming
class bag2_digital__latch_DICE_clk_sel(Module):
    """Module for library bag2_digital cell latch_DICE_clk_sel.

    Fill in high level description here.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'latch_DICE_clk_sel.yaml'))


    def __init__(self, database, parent=None, prj=None, **kwargs):
        Module.__init__(self, database, self.yaml_file, parent=parent, prj=prj, **kwargs)

    @classmethod
    def get_params_info(cls) -> Mapping[str, str]:
        # type: () -> Dict[str, str]
        """Returns a dictionary from parameter names to descriptions.

        Returns
        -------
        param_info : Optional[Dict[str, str]]
            dictionary from parameter names to descriptions.
        """
        return dict(
            l_dict='Channel length dictionary (gate_n/p, gate_in/out_n/p, latch_n/p, latch_in/out_n/p). In/out is for the tristates inner/outer devices.',
            w_dict='Channel width dictionary (gate_n/p, gate_in/out_n/p, latch_n/p, latch_in/out_n/p)',
            th_dict='Device flavor dictionary (gate_n/p, gate_in/out_n/p, latch_n/p, latch_in/out_n/p)',
            seg_dict='Number of fingers dictionary (gate_n/p, gate_in/out_n/p, latch_n/p, latch_in/out_n/p)'
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
        l_dict = params['l_dict']
        w_dict = params['w_dict']
        th_dict = params['th_dict']
        seg_dict = params['seg_dict']

        idx_key_map = ['latch_out',
                       'latch',
                       'latch_out',
                       'latch',
                       'gate_out',
                       'gate_in',
                       'gate',
                       'latch_in',
                       'latch_in']

        for i, k in enumerate(idx_key_map):
            for mos_type in ['n', 'p']:
                k_full = f'{k}_{mos_type}'
                inst_name = f'{mos_type.upper()}{i}'
                device_params = dict(l=l_dict[k_full],
                                     w=w_dict[k_full],
                                     intent=th_dict[k_full],
                                     nf=seg_dict[k_full])
                self.instances[inst_name].design(**device_params)
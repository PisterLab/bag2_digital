# -*- coding: utf-8 -*-

from typing import Dict, Mapping

import os
import pkg_resources

from bag.design.module import Module


# noinspection PyPep8Naming
class bag2_digital__latch_DICE_tgate_sel(Module):
    """Module for library bag2_digital cell latch_DICE_tgate_sel.

    Fill in high level description here.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'latch_DICE_tgate_sel.yaml'))


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
            sw_type='switch_mos type is p, n, or both for PMOS, NMOS, or transmission gate respectively',
            l_dict='Channel length dictionary (sw, latch_n, latch_p)',
            w_dict='Channel width dictionary (sw, latch_n, latch_p)',
            th_dict='Device flavor dictionary (sw, latch_n, latch_p)',
            seg_dict='Number of fingers dictionary (sw, latch_n, latch_p)'
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
        sw_type = params['sw_type']
        l_dict = params['l_dict']
        w_dict = params['w_dict']
        th_dict = params['th_dict']
        seg_dict = params['seg_dict']

        # Remove any unnecessary clock pins
        if sw_type == 'p':
            self.remove_pin('CLKb')
        elif sw_type == 'n':
            self.remove_pin('CLK')

        # Design switches
        sw_params_dict = dict()
        if sw_type != 'p':
            n_params_dict = dict(nf=seg_dict['sw_n'],
                                 w=w_dict['sw_n'],
                                 l=l_dict['sw_n'],
                                 intent=th_dict['sw_n'])
            sw_params_dict['n'] = n_params_dict
        if sw_type != 'n':
            p_params_dict = dict(nf=seg_dict['sw_p'],
                                 w=w_dict['sw_p'],
                                 l=l_dict['sw_p'],
                                 intent=th_dict['sw_p'])
            sw_params_dict['p'] = p_params_dict
        self.instances['XSW4'].design(mos_type=sw_type, mos_params_dict=sw_params_dict)
        self.instances['XSW5'].design(mos_type=sw_type, mos_params_dict=sw_params_dict)

        inst_key_map = dict()
        # Design other transistors
        for i in range(4):
            inst_key_map[f'N{i}'] = 'latch_n'
            inst_key_map[f'P{i}'] = 'latch_p'

        for inst, k in inst_key_map.items():
            device_params = dict(l=l_dict[k],
                                 w=w_dict[k],
                                 intent=th_dict[k],
                                 nf=seg_dict[k])
            self.instances[inst].design(**device_params)


# -*- coding: utf-8 -*-

from typing import Dict, Mapping

import os
import pkg_resources

from bag.design.module import Module


# noinspection PyPep8Naming
class bag2_digital__latch_DICE(Module):
    """Module for library bag2_digital cell latch_DICE.

    Fill in high level description here.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'latch_DICE.yaml'))


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
            l_dict = 'Channel length dictionary (sw, latch_n, latch_p)',
            w_dict = 'Channel width dictionary (sw, latch_n, latch_p)',
            th_dict = 'Device flavor dictionary (sw, latch_n, latch_p)',
            seg_dict = 'Number of fingers dictionary (sw, latch_n, latch_p)'
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

        inst_key_map = dict(N4='sw',
                            N5='sw')
        for i in range(4):
            inst_key_map[f'N{i}'] = 'latch_n'
            inst_key_map[f'P{i}'] = 'latch_p'

        for inst, k in inst_key_map.items():
            device_params = dict(l=l_dict[k],
                                 w=w_dict[k],
                                 intent=th_dict[k],
                                 nf=seg_dict[k])
            self.instances[inst].design(**device_params)
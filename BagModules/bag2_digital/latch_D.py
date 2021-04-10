# -*- coding: utf-8 -*-

from typing import Dict, Mapping

import os
import pkg_resources

from bag.design.module import Module


# noinspection PyPep8Naming
class bag2_digital__latch_D(Module):
    """Module for library bag2_digital cell latch_D.

    Fill in high level description here.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'latch_D.yaml'))


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
            lch = 'Channel length',
            th_dict = 'Dictionary of threshold flavors. inv_n/p, latch_n/p, nand_n/p',
            w_dict = 'Dictionary of channel widths. inv_n/p, latch_n/p, nand_n/p',
            seg_dict = 'Dictionary of number of fingers. inv_n/p, latch_n/p, nand_n/p'
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
        lch = params['lch']
        th_dict = params['th_dict']
        w_dict = params['w_dict']
        seg_dict = params['seg_dict']

        ### Design instances
        latch_params = dict(seg_n=seg_dict['latch_n'],
                            seg_p=seg_dict['latch_p'],
                            w_n=w_dict['latch_n'],
                            w_p=w_dict['latch_p'],
                            th_n=th_dict['latch_n'],
                            th_p=th_dict['latch_p'],
                            lch=lch)

        nand_params = dict(seg_n=seg_dict['nand_n'],
                           seg_p=seg_dict['nand_p'],
                           w_n=w_dict['nand_n'],
                           w_p=w_dict['nand_p'],
                           th_n=th_dict['nand_n'],
                           th_p=th_dict['nand_p'],
                           lch=lch,
                           num_in=2)
        inv_params = dict(seg_n=seg_dict['inv_n'],
                          seg_p=seg_dict['inv_p'],
                          w_n=w_dict['inv_n'],
                          w_p=w_dict['inv_p'],
                          th_n=th_dict['inv_n'],
                          th_p=th_dict['inv_p'],
                          lch=lch, stack_n=1, stack_p=1)

        self.instances['XINV'].design(**inv_params)
        self.instances['XNANDSb'].design(**nand_params)
        self.instances['XNANDRb'].design(**nand_params)
        self.instances['XLATCH'].design(**latch_params)

        ### Rewire
        self.reconnect_instance_terminal('XNANDSb', 'in<1:0>', 'Db,CLK')
        self.reconnect_instance_terminal('XNANDRb', 'in<1:0>', 'D,CLK')
# -*- coding: utf-8 -*-

from typing import Mapping, Any

import os
import pkg_resources

from bag.design.module import Module


# noinspection PyPep8Naming
class bag2_digital__nor(Module):
    """Module for library bag2_digital cell nor.

    Fill in high level description here.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'nor.yaml'))


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
            seg_n = 'NMOS number of fingers',
            seg_p = 'PMOS number of fingers',
            w_n = 'NMOS width',
            w_p = 'PMOS width',
            th_n = 'NMOS threshold flavor',
            th_p = 'PMOS threshold flavor',
            lch = 'Channel length',
            num_in = 'Number of inputs',
        )

    # @classmethod
    # def get_default_params_info(cls) -> Mapping[str,Any]:
    #     return dict(
    #             seg_n=1,
    #             seg_p=1,
    #             num_in=2,
    #         )

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
        num_in = params['num_in']

        assert num_in > 1, 'Number of inputs must be > 1'

        suffix_in = f'<{num_in-1}:0>'

        # Design instancess
        self.instances['XP'].design(
            lch = params['lch'],
            w = params['w_p'],
            stack = num_in,
            intent = params['th_p'],
            seg = params['seg_p'],
            export_mid = False)

        self.reconnect_instance_terminal('XP', f'G{suffix_in}', f'in{suffix_in}')

        self.instances['XN'].design(
            lch = params['lch'],
            w = params['w_n'],
            stack = 1,
            intent = params['th_n'],
            seg = params['seg_n'],
            export_mid = False)

        self.array_instance('XN', [f'XN{suffix_in}'], term_list=[dict(G=f'in{suffix_in}',
                                                                      D='out',
                                                                      S='VSS',
                                                                      B='VSS')])

        # Rename pins appropriately
        self.rename_pin('in', f'in{suffix_in}')
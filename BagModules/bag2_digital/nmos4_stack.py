# -*- coding: utf-8 -*-

from typing import Mapping

import os
import pkg_resources

from bag.design.module import Module


# noinspection PyPep8Naming
class bag2_digital__nmos4_stack(Module):
    """Module for library bag2_digital cell nmos4_stack.

    Fill in high level description here.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'nmos4_stack.yaml'))


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
            lch = 'Channel length in resolution units',
            w = 'Channel width in resolution units',
            stack = 'Number of stacked devices',
            intent = 'Threshold flavor',
            seg = 'Number of segments per device.',
            export_mid = 'True to export intermediate nodes',
        )

    def design(self, **params) -> None:
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
        w = params['w']
        stack = params['stack']
        intent = params['intent']
        seg = params['seg']
        export_mid = params['export_mid']

        # Designing instances
        self.instances['XN'].design(w=w, l=lch, nf=seg, intent=intent)

        if stack > 1:
            # Getting new connections with the stack
            if stack == 2:
                mid_name = 'm'
            else:
                mid_name = ','.join([f'm<{i}>' for i in range(stack-1)])

            d_conn = ','.join([mid_name, 'D'])
            s_conn = ','.join(['S', mid_name])
            g_conn = f'G<{stack-1}:0>'
            term_list = [dict(D=d_conn, S=s_conn, G=g_conn)]

            # Renaming instances
            self.array_instance('XN', [f'XN<{stack-1}:0>'], term_list=term_list)

            # Renaming pins
            self.rename_pin('G', f'G<{stack-1}:0>')

            if export_mid:
                suffix_mid = '' if stack == 2 else f'<{stack-2}:0>'
                self.add_pin(f'm{suffix_mid}', 'inputOutput')
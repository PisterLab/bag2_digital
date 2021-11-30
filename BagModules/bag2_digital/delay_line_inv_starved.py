# -*- coding: utf-8 -*-

from typing import Dict, Mapping
from warnings import warn

import os
import pkg_resources

from bag.design.module import Module


# noinspection PyPep8Naming
class bag2_digital__delay_line_inv_starved(Module):
    """Module for library bag2_digital cell delay_line_inv_starved.
    Current-starved inverter with up to one device above and below the main
    inverter.

    Fill in high level description here.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'delay_line_inv_starved.yaml'))


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
            num_inv='Integer. Number of inverters to include in the delay line.',
            inv_tristate_params='Tristate inverter parameters',
            export_outb='True to pin out all inverter outputs. False to pin out every other inverter output.'
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
        num_inv             = params['num_inv']
        inv_tristate_params = params['inv_tristate_params']
        export_outb         = params['export_outb']

        # Determine which side(s) have stacking
        nstack      = inv_tristate_params['nstack_params']['stack']
        pstack      = inv_tristate_params['pstack_params']['stack']
        has_ngate   = nstack > 1
        has_pgate   = pstack > 1

        assert has_ngate or has_pgate, \
            f'Must have a supply gate device on P and/or N side'
        assert num_inv >= 1, f'Number of inverters {num_inv} must be >= 1'

        # Keeping track of output indexing
        num_out = num_inv // 2
        num_outb = num_inv - num_out

        suffix_out = f'<{num_out-1}:0>' if num_out > 1 else ''
        suffix_outb = f'<{num_outb-1}:0>' if num_outb > 1 else ''
        suffix_ins = f'<{num_outb-2}:0>' if num_out > 1 else ''

        if not export_outb and num_inv%2==1:
            warn(f'(delay_line_inv_starved) Unused final inverter')

        # Array (or remove) and design devices
        if num_out > 1:
            self.array_instance('XINV1', [f'XINV1{suffix_out}'], [{'in' : f'outb{suffix_out}', 
                                                                'out' : f'out{suffix_out}',
                                                                'VP' : 'VP',
                                                                'VN' : 'VN',
                                                                'VDD' : 'VDD',
                                                                'VSS' : 'VSS'}])
            self.instances['XINV1'][0].design(**inv_tristate_params)
        elif num_out == 1:
            self.instances['XINV1'].design(**inv_tristate_params)
        else:
            self.delete_instance('XINV1')

        if num_outb > 1:
            self.array_instance('XINV0', [f'XINV0{suffix_outb}'], [{'in' : f'out{suffix_ins},in', 
                                                                'out' : f'outb{suffix_outb}',
                                                                'VP' : 'VP',
                                                                'VN' : 'VN',
                                                                'VDD' : 'VDD',
                                                                'VSS' : 'VSS'}])
            self.instances['XINV0'][0].design(**inv_tristate_params)
        elif num_outb == 1:
            self.instances['XINV0'].design(**inv_tristate_params)

        # Remove and rename pins as necessary
        if not export_outb:
            self.remove_pin('outb')
        elif num_outb > 1:
            self.rename_pin('outb', f'outb{suffix_outb}')

        if num_out > 1:
            self.rename_pin('out', f'out{suffix_out}')

        if not has_ngate:
            self.remove_pin('VN')

        if not has_pgate:
            self.remove_pin('VP')

        self.instances['XINV0']
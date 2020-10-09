# -*- coding: utf-8 -*-

from typing import Mapping, Any

import os
import pkg_resources
from re import findall

from bag.design.module import Module


# noinspection PyPep8Naming
class bag2_digital__inv_chain(Module):
    """Module for library bag2_digital cell inv_chain.

    Fill in high level description here.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'inv_chain.yaml'))


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
            inv_param_list = 'List of inv parameters, starting from the front.',
            dual_output = 'True to have outb and out. Only used if there is more than one device.'
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
        num_devices = len(params['inv_param_list'])
        assert num_devices >= 1, f'Number of devices {num_devices} must be >= 1'

        # Check if the output is inverting (relative to input)
        out_inv = num_devices % 2 == 1

        # Arraying and connecting instances
        inst_conn_dict = dict()
        inst_params_dict = dict()

        idx_out = num_devices-1 if num_devices%2==0 else num_devices-2
        idx_outb = num_devices-1 if num_devices%2==1 else num_devices-2

        out_conn = 'in'
        for i in range(num_devices):
            in_conn = out_conn

            if i == idx_out:
                out_conn = 'out'
            elif i == idx_outb:
                out_conn = 'outb'
            else:
                out_conn = f'm<{i}>'
            
            inst_conn_dict[f'XINV<{i}>'] = {'in' : in_conn,
                                            'out' : out_conn,
                                            'VDD' : 'VDD',
                                            'VSS': 'VSS'}
            inst_params_dict[i] = params['inv_param_list'][i]

        inst_name_list = list(inst_conn_dict.keys())
        inst_term_list = [inst_conn_dict[name] for name in inst_name_list]

        self.array_instance('XINV', inst_name_list, inst_term_list)

        # Designing instances
        for idx_inst, inst_params in inst_params_dict.items():
            self.instances['XINV'][idx_inst].design(**inst_params)

        # For dual output, remove pins as necessary
        if not params['dual_output']:
            pin_unused = 'out' if out_inv else 'outb'
            self.remove_pin(pin_unused)
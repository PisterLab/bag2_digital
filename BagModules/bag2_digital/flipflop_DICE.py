# -*- coding: utf-8 -*-

from typing import Dict, Mapping

import os
import pkg_resources

from bag.design.module import Module


# noinspection PyPep8Naming
class bag2_digital__flipflop_DICE(Module):
    """Module for library bag2_digital cell flipflop_DICE.

    Fill in high level description here.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'flipflop_DICE.yaml'))


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
            diff_clk='True to have a differential input clock',
            pos_edge='True to trigger on a rising edge (single-ended clock only)',
            master_params = 'Master D latch parameters',
            slave_params = 'Slave D latch parameters',
            inv_params = 'Clock inverter parameters',
        )

    def design(self, **params):
        """
        """
        diff_clk = params['diff_clk']
        pos_edge = params['pos_edge']
        master_params = params['master_params']
        slave_params = params['slave_params']
        inv_params = params['inv_params']

        ### Case 1: Single-ended clock (negative edge triggered)
        if not diff_clk:
            # Remove unnecessary pins and clock buffers
            pin_rm = 'CLKb_IN' if pos_edge else 'CLK_IN'
            self.remove_pin(pin_rm)
            self.delete_instance('XINV_CLKb')

            # Design clock buffer
            self.instances['XINV_CLK'].design(stack_n=1, stack_p=1, **inv_params)

            # Rewiring the clock buffer
            buf_conn_dict = {'in' : 'CLK_IN' if pos_edge else 'CLKb_IN',
                             'out' : 'CLKb' if pos_edge else 'CLKbb'}
            for pin, net in buf_conn_dict.items():
                self.reconnect_instance_terminal('XINV_CLK', pin, net)

            # Replace the latches to not have differential clock
            self.replace_instance_master(inst_name='XM',
                                         lib_name='bag2_digital',
                                         cell_name='latch_DICE_clk')
            self.replace_instance_master(inst_name='XS',
                                         lib_name='bag2_digital',
                                         cell_name='latch_DICE_clk')

            # Reconnect the latches
            master_conn_dict = dict(D='D_IN',
                                    CLK='CLKb' if pos_edge else 'CLKb_in',
                                    Q='Qm',
                                    VDD='VDD',
                                    VSS='VSS')

            slave_conn_dict = dict(D='Qm',
                                   CLK='CLK_IN' if pos_edge else 'CLKbb',
                                   Q='Q_OUT',
                                   VDD='VDD',
                                   VSS='VSS')

            for pin, net in master_conn_dict.items():
                self.reconnect_instance_terminal('XM', pin, net)
            for pin, net in slave_conn_dict.items():
                self.reconnect_instance_terminal('XS', pin, net)

        ### Case 2: Differential clock
        else:
            self.instances['XINV_CLK'].design(stack_n=1, stack_p=1, **inv_params)
            self.instances['XINV_CLKb'].design(stack_n=1, stack_p=1, **inv_params)

        ### Design latches
        self.instances['XM'].design(**master_params)
        self.instances['XS'].design(**slave_params)
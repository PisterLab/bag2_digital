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
            latch_type = 'inv or tgate for inverter-based or transmission gate latch',
            diff_clk='True to have a differential input clock (if applicable',
            pos_edge='True to trigger on a rising edge (single-ended clock only)',
            latch_params = 'Latch parameters',
            inv_params = 'Clock inverter parameters',
        )

    def design(self, **params):
        """
        """
        latch_type = params['latch_type']
        diff_clk = params['diff_clk']
        pos_edge = params['pos_edge']
        latch_params = params['latch_params']
        inv_params = params['inv_params']

        latch_clk = True
        latch_clkb = True

        assert latch_type in ('inv', 'tgate'), "Latch type must be inv or tgate"
        if latch_type == 'tgate':
            self.replace_instance_master('XM', 'bag2_digital', 'latch_DICE_tgate_sel')
            self.replace_instance_master('XS', 'bag2_digital', 'latch_DICE_tgate_sel')
            if latch_params['sw_type'] != 'both':
                diff_clk = False
                latch_clk = latch_params['sw_type'] == 'n'
                latch_clkb = latch_params['sw_type'] = 'p'

        ### Case 1: Single-ended clock
        if not diff_clk:
            # Remove unnecessary pin
            pin_rm = 'CLKb_IN' if pos_edge else 'CLK_IN'
            self.remove_pin(pin_rm)

            # Rewire clock buffers
            master_clk_conn = 'CLKb' if pos_edge else 'CLK_IN'
            master_clkb_conn = 'CLK_IN' if pos_edge else 'CLKb'
            slave_clk_conn = 'CLKbb' if pos_edge else 'CLKb'
            slave_clkb_conn = 'CLKb' if pos_edge else 'CLKbb'
            if pos_edge:
                self.reconnect_instance_terminal('XINV_CLKb', 'in', 'CLKb')
                # self.reconnect_instance_terminal('XM', 'CLK', 'CLKb')
            else:
                self.reconnect_instance_terminal('XINV_CLK', 'in', 'CLKbb')
                # self.reconnect_instance_terminal('XM', 'CLKb', 'CLK')

            self.reconnect_instance_terminal('XM', 'CLK', master_clk_conn)
            self.reconnect_instance_terminal('XM', 'CLKb', master_clkb_conn)
            self.reconnect_instance_terminal('XS', 'CLK', slave_clk_conn)
            self.reconnect_instance_terminal('XS', 'CLKb', slave_clkb_conn)

        elif not pos_edge:
            self.reconnect_instance_terminal('XM', 'CLK', 'CLK_IN')
            self.reconnect_instance_terminal('XM', 'CLKb', 'CLKb')
            self.reconnect_instance_terminal('XS', 'CLK', 'CLKb_IN')
            self.reconnect_instance_terminal('XS', 'CLKb', 'CLKbb')

        # ### Case 1: Single-ended clock (negative edge triggered)
        # if not diff_clk:
        #     # Remove unnecessary pins and clock buffers
        #     pin_rm = 'CLKb_IN' if pos_edge else 'CLK_IN'
        #     self.remove_pin(pin_rm)
        #     self.delete_instance('XINV_CLKb')
        #
        #     # Design clock buffer
        #     self.instances['XINV_CLK'].design(stack_n=1, stack_p=1, **inv_params)
        #
        #     # Rewiring the clock buffer
        #     buf_conn_dict = {'in' : 'CLK_IN' if pos_edge else 'CLKb_IN',
        #                      'out' : 'CLKb' if pos_edge else 'CLKbb'}
        #     for pin, net in buf_conn_dict.items():
        #         self.reconnect_instance_terminal('XINV_CLK', pin, net)
        #
        #     # Replace the latches to not have differential clock
        #     if latch_type == 'inv':
        #         self.replace_instance_master(inst_name='XM',
        #                                      lib_name='bag2_digital',
        #                                      cell_name='latch_DICE_clk')
        #         self.replace_instance_master(inst_name='XS',
        #                                      lib_name='bag2_digital',
        #                                      cell_name='latch_DICE_clk')
        #
        #     # Reconnect the latches
        #     master_conn_dict = dict(D='D_IN',
        #                             CLK='CLKb' if pos_edge else 'CLKb_in',
        #                             Q='Qm',
        #                             VDD='VDD',
        #                             VSS='VSS')
        #
        #     slave_conn_dict = dict(D='Qm',
        #                            CLK='CLK_IN' if pos_edge else 'CLKbb',
        #                            Q='Q_OUT',
        #                            VDD='VDD',
        #                            VSS='VSS')
        #
        #     for pin, net in master_conn_dict.items():
        #         self.reconnect_instance_terminal('XM', pin, net)
        #     for pin, net in slave_conn_dict.items():
        #         self.reconnect_instance_terminal('XS', pin, net)
        #
        # ### Case 2: Differential clock
        # else:
        #     self.instances['XINV_CLK'].design(stack_n=1, stack_p=1, **inv_params)
        #     self.instances['XINV_CLKb'].design(stack_n=1, stack_p=1, **inv_params)

        ### Design latches
        self.instances['XM'].design(**latch_params)
        self.instances['XS'].design(**latch_params)

        ### Design buffers
        self.instances['XINV_CLK'].design(stack_n=1, stack_p=1, **inv_params)
        self.instances['XINV_CLKb'].design(stack_n=1, stack_p=1, **inv_params)
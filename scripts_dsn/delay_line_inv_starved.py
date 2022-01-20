# -*- coding: utf-8 -*-

from typing import Mapping, Tuple, Any, List

import os
import pkg_resources
import numpy as np
import warnings

from bag.design.module import Module
from . import DesignModule, get_mos_db, estimate_vth, parallel, verify_ratio, num_den_add
from bag.data.lti import LTICircuit, get_w_3db, get_stability_margins, get_w_crossings
from bag.core import BagProject
from bag.util.search import BinaryIterator

# noinspection PyPep8Naming
class bag2_digital_delay_line_inv_starved_dsn(DesignModule):
    """Module for library bag2_digital cell delay_line_inv_starved.

    Fill in high level description here.
    """

    @classmethod
    def get_params_info(cls) -> Mapping[str,str]:
        # type: () -> Dict[str, str]
        """Returns a dictionary from parameter names to descriptions.

        Returns
        -------
        param_info : Optional[Dict[str, str]]
            dictionary from parameter names to descriptions.
        """
        ans = super().get_params_info()
        ans.update(dict(
            specfile_dict = 'Transistor database spec file names for each device. Keys n/pinner, n/pouter',,
            l_dict = 'Transistor channel length directory.',
            w_dict = 'Transistor channel width directory.',
            th_dict = 'Transistor flavor directory',
            seg_dict = 'Number of fingers in innermost transistors. Keys n and p.',
            num_inv = 'Integer. Number of inverters to include in the delay line.',
            sim_env = 'Simulation environment, i.e. corner name',
            vdd = 'Supply voltage in volts.',
            tdelay_rise = 'Target rising edge total delay from the input to the last noninverting input. None for don\'t care.',
            tdelay_fall = 'Target falling edge total delay from the input to the last noninverting input. None for don\'t care.',
            ctrl_type = 'p, n, or both for P-side, N-side, or both-side control devices.',
            vp_range = '(Min, max) of P-side control voltage, in volts. Unused if no P-side control exists.',
            vn_range = '(Min, max) of N-side control voltage, in volts. Unused if no N-side control exists.',
            cload = 'Output load capacitance in farads.',
            optional_params = 'Optional parameters. error_tol, vmid_in_r, vmid_out_r, vmid_in_f, vmid_out_f'
        ))
        return ans

    def meet_spec(self, **params) -> List[Mapping[str,Any]]:
        """To be overridden by subclasses to design this module.
        Returns collection of all possible solutions.
        Raises a ValueError if there is no solution.
        """
        optional_params = params['optional_params']

        ### Get DBs for each device
        specfile_dict = params['specfile_dict']
        l_dict = params['l_dict']
        th_dict = params['th_dict']
        sim_env = params['sim_env']
        
        # Databases
        db_dict = {k:get_mos_db(spec_file=specfile_dict[k],
                                intent=th_dict[k],
                                sim_env=sim_env,
                                lch=l_dict[k]) for k in specfile_dict.keys()}

        viable_op_list = []

        ### Simulate
        num_inv = params['num_inv']
        seg_dict = params['seg_dict']
        ctrl_type = params['ctrl_type']
        (vp_min, vp_max) = params['vp_range']
        (vn_min, vn_max) = params['vn_range']
        cload = params['cload']

        vdd = params['vdd']
        tr_target = params['tdelay_rise']
        tf_target = params['tdelay_fall']

        has_nctrl = ctrl_type.lower() in ('both', 'n')
        has_pctrl = ctrl_type.lower() in ('both', 'p')
        nstack = 2 if has_nctrl else 1
        pstack = 2 if has_pctrl else 1

        error_tol = optional_params.get('error_tol', 0.05)
        vmid_in_r = optional_params.get('vmid_in_r', vdd/3)
        vmid_out_r = optional_params.get('vmid_out_r', vdd/3)
        vmid_in_f = optional_params.get('vmid_in_f', vdd*2/3)
        vmid_out_f = optional_params.get('vmid_out_f', vdd*2/3)

        # Getting a starting point
        tb_params = dict(cload=cload,
            vn=(vn_min+vn_max)/2,
            vp=(vp_min+vp_max)/2,
            vdd=vdd,
            vss=0,
            vlow=vdd*0.1,
            vhigh=vdd*0.9,
            tstop=max(tr_target, tf_target)*2)

        nstack_params = dict(stack=nstack,
            lch_list=[l_dict['nouter'], l_dict['ninner']] if has_nctrl else [l_dict['ninner']],
            w_list=[w_dict['nouter'], w_dict['ninner']] if has_nctrl else [w_dict['ninner']],
            intent_list=[th_dict['nouter'], th_dict['ninner']] if has_nctrl else [th_dict['ninner']],
            seg_list=[seg_dict['n']]*nstack,
            export_mid=False)

        pstack_params = dict(stack=pstack,
            lch_list=[l_dict['pouter'], l_dict['pinner']] if has_nctrl else [l_dict['pinner']],
            w_list=[w_dict['pouter'], w_dict['pinner']] if has_nctrl else [w_dict['pinner']],
            intent_list=[th_dict['pouter'], th_dict['pinner']] if has_nctrl else [th_dict['pinner']],
            seg_list=[seg_dict['p']]*pstack,
            export_mid=False)

        dut_params = dict(num_inv=num_inv,
            export_outb=True,
            inv_tristate_params=dict(nstack_params=nstack_params,
                                    pstack_params=pstack_params))

        tb_params['dut_params'] = dut_params

        # Generate testbench
        bprj = BagProject()
        tb_name = get_tb_name()
        print(f'Creating testbench {tb_name}')
        tb_sch = prj.create_design_module(tb_lib, tb_cell)
        tb_sch.design(**tb_params)
        tb_sch.implement_design(impl_lib, top_cell_name=tb_name)
        tb_obj = prj.configure_testbench(impl_lib, tb_name)

        # P branch: binary search outermost device size for rise time
        if tr_target != None:
            nf_pouter_iter = BinaryIterator(1, None, 1)
            while nf_pouter_iter.has_next():
                pstack_params['seg_list'][0] = nf_pouter_iter.get_next()
                tprop_dict = meas(prj=bprj,
                    tb_sch=tb_sch,
                    tb_obj=tb_obj,
                    tb_params=tb_params,
                    vmid_in_r=vmid_in_r,
                    vmid_out_r=vmid_out_r,
                    vmid_in_f=vmid_in_f,
                    vmid_out_f=vmid_out_f)


        # N branch: binary search outermost device size for fall time
        nf_nouter_iter = BinaryIterator(1, None, 1)

        # Final simulation for rise and fall times

        return viable_op_list

    

    def op_compare(self, op1:Mapping[str,Any], op2:Mapping[str,Any]):
        """Returns the best operating condition based on 
        minimizing bias current.
        """
        # return op2 if op1['ibias'] > op2['ibias'] else op1
        # return op2 if op2['ugf'] > op1['ugf'] else op1
        return op2 if op2['fbw'] > op1['fbw'] else op1

    def get_sch_params(self, op):
        l_dict = self.other_params['l_dict']
        w_dict = self.other_params['w_dict'] 
        seg_dict = {'in' : op['nf_in'],
                    'tail' : op['nf_tail'],
                    'load' : op['nf_load'],
                    'bias' : op['nf_bias']}

        for k, v in l_dict.items():
            l_dict[k] = float(v)
            
        for k, v in w_dict.items():
            w_dict[k] = float(v)
            
        for k, v in seg_dict.items():
            seg_dict[k] = int(v)
        
        return dict(in_type=self.other_params['in_type'],
                    l_dict=l_dict,
                    w_dict=w_dict,
                    th_dict=self.other_params['th_dict'],
                    seg_dict=seg_dict)
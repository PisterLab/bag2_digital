# -*- coding: utf-8 -*-

from typing import Dict, Mapping

import os
import pkg_resources

from bag.design.module import Module


# noinspection PyPep8Naming
class bag2_digital__flipflop_D(Module):
    """Module for library bag2_digital cell flipflop_D.

    Fill in high level description here.
    """
    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'flipflop_D.yaml'))


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
            has_set = 'True to include a set (bar) pin, i.e. set=1 -> Q=1,Qb=0',
            has_clr = 'True to include a clear (bar) pin, i.e. clr=1 -> Q=0,Qb=1',
            lch = 'Channel length',
            th_dict = 'Device flavor dictionary. in_n/p, out_n/p',
            w_dict = 'Channel width dictionary. in_n/p, out_n/p',
            seg_dict = 'Number of fingers dictionary. in_n/p, out_n/p'
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
        has_set = params['has_set']
        has_clear = params['has_clr']
        lch = params['lch']
        w_dict = params['w_dict']
        th_dict = params['th_dict']
        seg_dict = params['seg_dict']

        ### Design instances
        name_map = dict(XS='in',
                        XSb='in',
                        XRb='in',
                        XR='in',
                        XQ='out',
                        XQb='out')

        params_dict = dict()
        for k in ('in', 'out'):
            params_dict[k] = dict(num_in=3,
                                  lch=lch,
                                  w_p=w_dict[f'{k}_p'],
                                  w_n=w_dict[f'{k}_n'],
                                  th_p=th_dict[f'{k}_p'],
                                  th_n=th_dict[f'{k}_n'],
                                  seg_p=seg_dict[f'{k}_p'],
                                  seg_n=seg_dict[f'{k}_n'])

        for name, k in name_map.items():
            self.instances[name].design(**(params_dict[k]))

        ### Wiring instances
        if not has_clear:
            self.remove_pin('CLRb')
            clrb_conn = 'VDD'
        else:
            clrb_conn = 'CLRb'

        if not has_set:
            self.remove_pin('SETb')
            setb_conn = 'VDD'
        else:
            setb_conn = 'SETb'

        in_S = f'{setb_conn},R,Sb'
        in_Sb = f'{clrb_conn},CLK,S'
        in_Rb = 'CLK,Sb,R'
        in_R = f'D,{clrb_conn},Rb'
        in_Q = f'{setb_conn},Sb,Qb'
        in_Qb = f'{clrb_conn},Rb,Q'

        conn_map = dict(S=in_S,
                        Sb=in_Sb,
                        Rb=in_Rb,
                        R=in_R,
                        Q=in_Q,
                        Qb=in_Qb)

        for name, conn in conn_map.items():
            self.reconnect_instance_terminal(f'X{name}', f'in<2:0>', conn)
            self.reconnect_instance_terminal(f'X{name}', 'out', name)
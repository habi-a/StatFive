from Sod.models import Fonction as fun_

from Libs.misc import Misc as misc_

from collections import defaultdict as dd_

from multiprocessing import Process
from multiprocessing import Queue

import time




class Functions():

    def __init__(self):
        pass
    
    def functions(self,sys):
        """
        Give the function composition by sys
        return {sys:fun:{auth,auth...}...}
        """
        return misc_().do_dict_set([(e['Code_fonction'],e['Code_auto'])
                                    for e in fun_.objects.filter(system = sys).values('Code_auto','Code_fonction')
                                    ])

    def get_activated_functions(self,d_auth):
        """
        d_auth entry possible:
            if user : return : {sys:user:composite:role:profil:{auth,auth}...}
            if compo : return : {sys:composite:role:profil:{auth,auth}...}
            if single : return : {sys:role:prof:{auth,auth...}...}
        Give the activated function form d_auth
        return # if USER > d = {sys:user:function:auth:profil:role:compo}
               # if COMPO > d = {sys:compo:function:auth:profil:role}
               # if SINGLE > d = {sys:role:function:auth:profil}
        """
        # no auth activated
        s = set()
        d = dd_(dict)
        for sys in d_auth:
            if isinstance(d_auth[sys],str):
                pass
            else:
                d_functions = self.functions(sys)
                t = time.time()
                d_auths = misc_().do_dict_set(list(d_auth[sys]),2)
                s.update({tuple([e[-1],fun.split('@')[0],fun,fun.split('@')[1],auth]+list(e))
                          for key in d_auths
                          for fun in d_functions
                          if d_functions[fun].issubset(set(d_auths[key]))
                          for auth in d_functions[fun]
                          for e in d_auths[key][auth]
                          })               
        return s

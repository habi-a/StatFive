from Basis.models import Sys_Type as s

'''
from Libs.Sap.Role.Client.role import Role as r_
from Libs.Sap.Role.Client.roles import Roles as rs_
from Libs.Sap.User.Client.users import Users as usr_
'''

from Libs.misc import Misc as m

from Libs.Analysis.Client.orga import Orga as o
from Libs.Analysis.auths import Auths as a_
from Libs.Analysis.functions import Functions as f_
from Libs.Analysis.risks import Risks as r_

from Sod.models import Profil_orga

from copy import deepcopy

class Analysis():
    """
    SoD Analysis on demand
    Init = self for impacted system
    """
    
    def __init__(self,l_sys):
        self.l_sys = l_sys

    # chained auths > Func > Risk
    def launch_analysis(self,d = dict(),s = set()):
        """
        #######  d =kwargs for auth
        
        Method for seeking risk
        d as to be like in case of classique analysis
            for user {USERS :iterable}
            for compo {COLLECTIVES : iterable}
            for single {SINGLES : iterable}
        s as to be a set as prodive get_auths in case of impacted analysis
        
        return set of values
            for users >> {(user, compo, single, sys, obj, tcd, ssfun, risk),...}
            for compos >> {(compo, single, sys, obj, tcd, ssfun, risk),...}
            for singles >> {( single, sys, obj, tcd, ssfun, risk),...}
        """
        if s:
            return r_().get_activated_risks(
                          f_().get_activated_functions(s))
        return r_().get_activated_risks(
                      f_().get_activated_functions(
                            a_(self.l_sys).get_auths(**d)))
        

from Libs.Back.Sap.User.Client.users import Users as sap_users
from Basis.models import Sys_Type
from Libs.Back.misc import Misc as m_


class Users():

    def __init__(self,l_sys):
        self.dd_sys = m_().do_dict_set([[v for k,v in e.items()]
                                        for e in Sys_Type.objects.filter(system__in = l_sys).values('type_sys','system')])
        for type_sys in self.dd_sys:
            self.dd_sys[type_sys] = {sys:m_().get_sys_info(sys)
                                     for sys in self.dd_sys[type_sys]}

    def get(self, d_users = None, **kwargs):
        if not d_users:
            d_users = dict()
        if 'SAP' in self.dd_sys:
            d_users = m_().dict_merge(d_users, sap_users(self.dd_sys['SAP']).get(d_users,**kwargs))
        return d_users

    def change(self, *args, **kwargs):
        d = dict()
        if 'SAP' in self.dd_sys:
            d = m_().dict_merge(d, sap_users(self.dd_sys['SAP']).change(*args,**kwargs))
        return d


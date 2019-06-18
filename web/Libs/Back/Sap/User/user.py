from Libs.Back.Sap.misc import Misc as ms_
from Libs.Back.misc import Misc as m_

#from Basis.models import fields
#from Basis.models import fields_mapping

import datetime


class User():

    def __init__(self,account,l_sys = []):
        """
        Initialisation of a user
        :parameter : ld_sys (dictionnary list for pyrfc connection), account (string for SAP user)
        """
        self.ld_sys = [m_().get_sys_info(sys)
                       for sys in l_sys
                       if m_().get_sys_info(sys)]
        self.account = account.upper()

    def exist(self):
        """
        Check if self.account exist for all d_sys in ld_sys
        :parameter : ld_sys (dictionnary list for pyrfc connection), account (string for SAP user)
        :return : {d_sys:boolean, d_sys:Error,...}
        """
        d = dict()
        # queryset of existing Swing d_sys
        for d_sys in self.ld_sys:
            d[d_sys['sys_name']] = ms_().launch_fm(d_sys,
                                                 'BAPI_USER_EXISTENCE_CHECK',
                                                 # kwargs
                                                 **{'USERNAME' : self.account}
                                                 )
        return d
                        
    def unlock(self):
        """
        Unlock SAP user for each d_sys from ld_sys
        :parameter : ld_sys (dictionnary list for pyrfc connection), account (string for SAP user)
        :return : {d_sys:action result,d_sys:Error...} action directly perfomed in SAP
        """
        d = dict()
        for d_sys in self.ld_sys:
            d[d_sys['sys_name']] = ms_().launch_fm(d_sys,
                                                 'BAPI_USER_UNLOCK',
                                                 # kwargs
                                                 **{'USERNAME' : self.account}
                                                 )
        return d

    def lock(self):
        """
        Lock SAP user for each d_sys from ld_sys
        :parameter : ld_sys (dictionnary list for pyrfc connection), account (string for SAP user)
        :return : {d_sys:action result,d_sys:Error...} action directly perfomed in SAP
        """
        d = dict()
        for d_sys in self.ld_sys:
            d[d_sys['sys_name']] = ms_().launch_fm(d_sys,
                                                 'BAPI_USER_LOCK',
                                                 # kwargs
                                                 **{'USERNAME' : self.account}
                                                 )
        return d

    def check_able_to_be_unlocked(self):
        """
        Check if the SAP user can be unlocked
        None = not revelant
        True = revelant
        False = Admin Lock
        :parameter : self.ld_sys (dictionnary list for pyrfc connection), self.account (string for SAP user)
        :return : {'sys_name': True, 'sys_name': false ...}
        """
        d = dict()
        for d_sys in self.ld_sys:
            d[d_sys['sys_name']] = m_().read_table(d_sys,
                                                   **{'QUERY_TABLE' : 'USR02',
                                                      'OPTIONS' : ["BNAME EQ '%s'"%self.account],
                                                      'FIELDS' : ['UFLAG']}
                                                   )
        for key in d:
            if isinstance(d[key],str):
                d[key] = d[key]
                continue
            elif d[key] == ['0']:
                d[key] = None
            elif d[key] == ['128']:
                d[key] = True
            else:
                d[key] = False
        return d

    def check_validity_date(self):
        """
        Check if the SAP user can be unlocked
        True = End of validity date > today
        False = End of validity date in the past
        :parameter : self.ld_sys (dictionnary list for pyrfc connection), self.account (string for SAP user)
        :return : {'sys_name': True, 'sys_name': false ..., sys_name = Error}
        """
        today = datetime.date.today().strftime('%Y%m%d')
        d = dict()
        for d_sys in self.ld_sys:
            read_table = m_().read_table(d_sys,**{'QUERY_TABLE' : 'USR02',
                                                  'OPTIONS' : ["BNAME EQ '%s' AND"%self.account,
                                                               "(GLTGB EQ '00000000' OR GLTGB GE '%s')"%today],
                                                  'FIELDS' : ['GLTGB']}
                                         )
            if isinstance(read_table,str):
                d[d_sys['sys_name']] = read_table
            # read table is a list by desing
            else:
                # if read_table is filling
                if read_table:
                    d[d_sys['sys_name']] = True
                else:
                    d[d_sys['sys_name']] = False
        return d

    def change_validity_date(self,end_date = '99991231'):
        """
        Change the validity date for self.account in SAP directly
        the action type come form m_().get_bapi_status
        :parameter : self.ld_sys (dictionnary list for pyrfc connection), end_date (string like YYYYMMDD)
        :return : {d_sys:action result,d_sys:Error...} action directly perfomed in SAP
        """
        d = dict()
        for d_sys in self.ld_sys:
            d[d_sys['sys_name']] = ms_().launch_fm(d_sys,
                                                 'BAPI_USER_CHANGE',
                                                 #kwargs
                                                 **{'USERNAME' : self.account,
                                                    'LOGONDATA' : {'GLTGB':end_date},
                                                    'LOGONDATAX' : {'GLTGB':'X'}
                                                    }
                                                 )
        return d

    def change_user_group(self,usergroup):
        """
        Change the user_group for self.account in SAP directly
        the action type come form m_().get_bapi_status
        :parameter : self.ld_sys (dictionnary list for pyrfc connection), usergroup (string)
        :return : {d_sys:action result,d_sys:Error...} action directly perfomed in SAP
        """
        d = dict()
        for d_sys in self.ld_sys:
            d[d_sys['sys_name']] = ms_().launch_fm(d_sys,
                                                 'BAPI_USER_CHANGE',
                                                 #kwargs
                                                 **{'USERNAME' : self.account,
                                                    'LOGONDATA' : {'CLASS':usergroup},
                                                    'LOGONDATAX' : {'CLASS':'X'}
                                                    }
                                                 )
        return d

    def change_pwd(self,pwd):
        """
        Change the pwd for self.account in SAP directly
        the action type come form m_().get_bapi_status
        :parameter : str pwd 
        :return : {d_sys:action result,d_sys:Error...} action directly perfomed in SAP
        """
        d = dict()
        for d_sys in self.ld_sys:
            d[d_sys['sys_name']] = ms_().launch_fm(d_sys,
                                                 'BAPI_USER_CHANGE',
                                                 #kwargs
                                                 **{'USERNAME' : self.account,
                                                    'PASSWORD' : {'BAPIPWD':pwd},
                                                    'PASSWORDX' : {'BAPIPWD':'X'}
                                                    }
                                                 )

        return d

    def detail(self,*args):
        """
        Get the self.account detail
        *args = restiction on revelant value
        :return : {d_sys:detail ,d_sys:Error...}
        """
        d = dict()
        for d_sys in self.ld_sys:
            d_detail = ms_().launch_fm(d_sys,
                                     'BAPI_USER_GET_DETAIL',
                                     #kwargs
                                     **{'USERNAME' : self.account}
                                     )
            # if an error is raised (str >> Pyrfc, list >> selection of the user)
            if isinstance(d_detail,str) or isinstance(d_detail,list):
                d[d_sys['sys_name']] = d_detail
            elif not args:
                d[d_sys['sys_name']] = d_detail
            else:
                d[d_sys['sys_name']] = {arg.upper():d_detail[arg.upper()]
                                        for arg in args
                                        if arg.upper() in d_detail}
            

        return d

    def roles_assigment(self, **kwargs):
        """
        kwargs get 2 keys Available ADD and REM
        ADD for the roles set to self.account
        REM for the roles remove to self.account
        :return: {d_sys:SAP action}
        """
        d = dict()
        for d_sys in self.ld_sys:
            # list comprehension to ease the role assignement
            l_roles = ms_().read_table(d_sys,**{'QUERY_TABLE':'AGR_USERS',
                                                'OPTIONS':["UNAME EQ '%s' AND COL_FLAG EQ ''"%self.account],
                                                'FIELDS':['AGR_NAME','FROM_DAT','TO_DAT']}
                                       )
            l_roles = [{'AGR_NAME':e[0],'FROM_DAT':e[1],'TO_DAT':e[2]}
                       for e in l_roles]            
            if 'ADD' in kwargs:
                l_roles.extend([{'AGR_NAME':e}
                                for e in kwargs['ADD']
                                if e not in [role['AGR_NAME']
                                             for role in l_roles]
                                ])
            if 'REM' in kwargs:
                l_roles = [e
                           for e in l_roles
                           if e['AGR_NAME'] not in kwargs['REM']]
            d[d_sys['sys_name']] = ms_().launch_fm(d_sys,
                                                'BAPI_USER_ACTGROUPS_ASSIGN',
                                                **{'USERNAME':self.account,
                                                   'ACTIVITYGROUPS':l_roles})
        return d

    def roles_assigment_cua(self, **kwargs):
        """
        kwargs get 2 keys Available ADD and REM
        ADD for the roles set to self.account
        REM for the roles remove to self.account
        :return: {d_sys:SAP action}
        """
        d = dict()
        for d_sys in self.ld_sys:
            # list comprehension to ease the role assignement
            l_roles = ms_().read_table(d_sys,**{'QUERY_TABLE':'USLA04',
                                                'OPTIONS':["BNAME EQ '%s'"%self.account],
                                                'FIELDS':['SUBSYSTEM','AGR_NAME','FROM_DAT','TO_DAT']}
                                       )
            l_roles = [{'SUBSYSTEM':e[0],'AGR_NAME':e[1],'FROM_DAT':e[2],'TO_DAT':e[3]}
                       for e in l_roles]            
            if 'ADD' in kwargs:
                l_roles.extend([{'SUBSYSTEM':sys,'AGR_NAME':e}
                                for e in kwargs['ADD']
                                if e not in [role['AGR_NAME']
                                             for role in l_roles]
                                for sys in self.get_cua_subsys()
                                ])
            if 'REM' in kwargs:
                l_roles = [e
                           for e in l_roles
                           if e['AGR_NAME'] not in kwargs['REM']]
            d[d_sys['sys_name']] = ms_().launch_fm(d_sys,
                                                'BAPI_USER_LOCACTGROUPS_ASSIGN',
                                                **{'USERNAME':self.account,
                                                   'ACTIVITYGROUPS':l_roles})
        return d

    def get_cua_subsys(self):
        return []

    def create(self,**kwargs):
        """
        Method for creating user on SAP
        kwargs >> option de creation
        :return: {d_sys:SAP action}
        """
        d = dict()
        for d_sys in self.ld_sys:
            d[d_sys['sys_name']] = ms_().launch_fm(d_sys,
                                                'BAPI_USER_CREATE',
                                                **kwargs)
        return d

    def roles_unassigment(self):
        """
        Method for creating user on SAP
        kwargs >> option de creation
        :return: {d_sys:SAP action}
        """
        d = dict()
        for d_sys in self.ld_sys:
            d[d_sys['sys_name']] = ms_().launch_fm(d_sys,
                                                'BAPI_USER_ACTGROUPS_DELETE')
        return d

    def roles_unassigment_cua(self):
        """
        Method for creating user on SAP
        kwargs >> option de creation
        :return: {d_sys:SAP action}
        """
        d = dict()
        for d_sys in self.ld_sys:
            d[d_sys['sys_name']] = ms_().launch_fm(d_sys,
                                                'BAPI_USER_LOCACTGROUPS_DELETE')
        return d
                          
            
            
        
        

















    


   
                






            

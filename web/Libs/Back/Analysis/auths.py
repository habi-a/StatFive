from Sod.models import Profil_Autorisation as pa_
from Sod.models import Autorisation as auto_

from Libs.Sap.Profile.profiles import Profiles as ps_

from Libs.Sap.Role.Client.roles import Roles as rs_

from Libs.Sap.User.Client.users import Users as us_

from Libs.misc import Misc as m_

from Basis.models import Sys_Type as s_

from collections import defaultdict as dd_

class Auths():
    """
    Class for auths determination in case of SOD analysis
    kwargs available :
    WITH for adding auth / role
    WITHOUT for removing auth / role
    SYS for impacted system
    """
    def __init__(self,l_sys,**kwargs):
        # WITH > adding new auth / new role in case of analysis simulation
        #       for adding auth, put a set of auth {auth,auth,...}
        #       for adding role, put a list of tuple as [(compo,role),,, )]
        #       for adding role to user, put a tuple of tuple ((user,role),(user,role)...)
        # WITHOUT > removing auth / role in case of analysis during simulation
        #       for removing auth, put a set of auth
        #       for removing role, put a list of tuple
        #       for removing role to user, put a tuple of tuple
        # dict comprehension for filtering on available key
        self.l_sys = l_sys
        self.kwargs = {e:list(kwargs[e]) for e in kwargs if e in ['WITHOUT','WITH']}
        self.d_sys_type = {e['system']:e['type_sys'] for e in s_.objects.values('system', 'type_sys')}

    def get_auths(self,**kwargs):
        """
        Class for auths determination in case of SOD analysis
        kwargs available :
        USERS : for getting auths by users User must be a list
                return : {(single,auth,sys,single),}
        COLLECTIVES : for getting auths by roles Compo must be a list
                Compo is only a composite role
                return : {(compo,auth,sys,single,compo),}
        SINGLES : for getting auths by profiles PROLFILES must be a list
                   return : {(user,auth,sys,single,compo,user),}

        return False when no auth is activated

        """
        if 'SINGLES' in kwargs:
            return self._get_auth_from_singles(list(kwargs['SINGLES']))
        elif 'COLLECTIVES' in kwargs:
            return self._get_auth_from_compos(list(kwargs['COLLECTIVES']))
        elif 'USERS' in kwargs:
            return self._get_auth_from_users(list(kwargs['USERS']))
        else:
            return 'get_auths no auths return'
            
        

    def _get_auth_from_singles(self,l_singles):
        d = dict()
        for sys in self.l_sys:
            if self.d_sys_type[sys] == 'SAP':
                if self.kwargs:
                    # return [d_auth_before,d_auth_after] on simulation purpose
                    return self._sap_get_auth_from_singles_kw(sys,l_singles)
                else:
                    d.update(self._sap_get_auth_from_singles(sys,l_singles))
        return d

    def _sap_get_auth_from_singles(self,sys,l_singles):
        """
        list for profs
        return : {sys:role:auth:role...}
        """
        ds_profiles_roles = m_().do_dict_str([e[::-1]
                                              for e in rs_(sys).get_profiles(**{'AGR_NAME':l_singles})])
        if ds_profiles_roles:
            s = set()
            s.update({(ds_profiles_roles[e['Profil']],
                       e['Code_auto'],
                       sys,
                       ds_profiles_roles[e['Profil']])
                       for profs_ in [sorted(list(ds_profiles_roles))[x:x+990]
                                      for x in range(0,len(ds_profiles_roles),990)
                                      ]
                       for e in pa_.objects.filter(system = sys,
                                                   # restriction on profil by list comprehension
                                                   Profil__in = profs_
                                                   ).values('Code_auto',
                                                            'Profil')
                       }
                      )
            if s:
                return {sys:s}
            else:
                return {sys:'No Auth Activated'}
        else:  
            return {sys:'No Profile matchted'}

    def _sap_get_auth_from_singles_kw(self,sys,l_singles):
        """Return a list of dict after and before auth add/rem"""      
        s_before = self._sap_get_auth_from_singles(sys,l_singles)[sys]
        if isinstance(s_before,str):
            s_after = set()
        else:
            s_after = set(s_before)
        s_after.update({(role,auth,sys,role)
                        for role in l_singles
                        for auth in self.kwargs['WITH']})
        s_after = s_after-{(role,auth,sys,role)
                           for role in l_singles
                           for auth in self.kwargs['WITHOUT']}
        return [{sys:s_before},{sys:s_after}]
        
    def _get_auth_from_compos(self,l_compos):
        d = dict()
        for sys in self.l_sys:
            if self.d_sys_type[sys] == 'SAP':
                if self.kwargs:
                    # return [d_auth_before,d_auth_after] on simulation purpose
                    return self._sap_get_auth_from_compos_kw(sys,l_compos)
                else:
                    d.update(self._sap_get_auth_from_compos(sys,l_compos))
        return d

    def _sap_get_auth_from_compos(self,sys,l_compos):
        """return : {sys:composite:auth:{role,..}...}"""
        ds_single_compo = m_().do_dict_set([e[::-1]
                                           for e in rs_(sys).get_compos(**{'AGR_NAME':l_compos})
                                           ])
        if ds_single_compo:
            s_singles = self._sap_get_auth_from_singles(sys,list(ds_single_compo))[sys]

            # if at least one auth is activated
            if s_singles and isinstance(s_singles,set):
                s = set()
                s.update([tuple([compo]+list(single)[1:]+[compo])
                          for single in s_singles
                          for compo in ds_single_compo[single[0]]
                          ]
                         )
                return {sys:s}
            else: return {sys:'No Auth Activated on Collectives roles'}
        else:
            return {sys:set()}
        
    def _sap_get_auth_from_compos_kw(self,sys,l_compos):
        s_before = self._sap_get_auth_from_compos(sys,l_compos)[sys]
        if isinstance(s_before,set):
            s_after = set(s_before)
        else:
            s_after = set()
        if self.kwargs['WITH']:
            s_singles = self._sap_get_auth_from_singles(sys,self.kwargs['WITH'])[sys]
            if isinstance(s_singles,set): 
                s_after.update({tuple([compo]+list(single)[1:]+[compo])
                                for single in s_singles
                                for compo in l_compos
                                })
        
        if self.kwargs['WITHOUT']:
            s_after = s_after - {e
                                 for e in s_after
                                 if e[2] in self.kwargs['WITHOUT']
                                 }
        return [{sys:s_before},{sys:s_after}]

    def _get_auth_from_users(self,l_users):
        d = dict()
        for sys in self.l_sys:
            if self.d_sys_type[sys] == 'SAP':
                if self.kwargs:
                    # return [d_auth_before,d_auth_after] on simulation purpose
                    return self._sap_get_auth_from_users_kw(sys,l_users)
                else:
                    d.update(self._sap_get_auth_from_users(sys,l_users))
        return d

    def _sap_get_auth_from_user_profils(self,sys,l_prof):
        l_prof = [e[0]
                  for e in rs_(sys).get_profiles(**{'PROFILES':l_prof})
                  if e[0] == e[1]
                  ]
        # get the auth from direct profil assignement
        return {(e['Profil'],e['Code_auto'])
                for profs_ in [l_prof[x:x+990]
                               for x in range(0,len(l_prof),990)
                               ]
                for e in pa_.objects.filter(system = sys,
                                            Profil__in = profs_
                                            ).values('Code_auto',
                                                     'Profil')
                }
        

    def _sap_get_auth_from_users(self,sys,l_users):
        ds_prof_usr = m_().do_dict_set([(e[0][:10],e[1])
                                        for e in ps_(sys).get_assignations(**{'BNAME':l_users})
                                        ]
                                       )
        
        s_user_auth = set()
        # direct profil assigment
        s_user_auth.update({(user,e[1],sys,e[0],'',user)
                            for e in self._sap_get_auth_from_user_profils(sys,
                                                                          list(ds_prof_usr))
                            for user in ds_prof_usr[e[0]]
                            }
                           )
        ds_role_user = m_().do_dict_set(list({(e[1],e[0])
                                              for e in rs_(sys).get_assigment(**{'UNAME':l_users})
                                              if e[-1] != 'X'
                                              }
                                             )
                                        )
        if ds_role_user:
            # update ds_user_auth with de direct single role assigment
            s_user_auth.update({tuple([user]+list(role[1:])+['',user])
                                for role in self._sap_get_auth_from_singles(sys,
                                                                            list(ds_role_user)
                                                                            )[sys]
                                if isinstance(role,tuple)  
                                for user in ds_role_user[role[0]]                 
                                })
            # update ds_user_auth with de direct composite role assigment
            s_user_auth.update({tuple([user]+list(role[1:])+[user])
                                for role in self._sap_get_auth_from_compos(sys,
                                                                           list(ds_role_user)
                                                                           )[sys]
                                if isinstance(role,tuple)  
                                for user in ds_role_user[role[0]]                                        
                                })
        return {sys:s_user_auth}

    def _sap_get_auth_from_users_kw(self,sys,l_users):
        s_before = self._sap_get_auth_from_users(sys,l_users)[sys]
        #return : {sys:user:auth:role:{composite,...}...}
        if isinstance(s_before,set):
            s_after = set(s_before)
        else:
            s_after = set()
        # managing the role addition
        if self.kwargs['WITH']:
            # if roles are composite
            s_after.update({tuple([user]+list(e)[1:]+[user])
                            for e in self._sap_get_auth_from_compos(sys,
                                                                    self.kwargs['WITH']
                                                                    )[sys]
                            for user in l_users})
            # if role are single
            '''return : {sys:role:auth:role...}'''
            s_after.update({tuple([user]+list(e)[1:]+['',user])
                            for e in self._sap_get_auth_from_singles(sys,
                                                                     self.kwargs['WITH']
                                                                     )[sys]
                            for user in l_users})
        # managing the role deletion
        if self.kwargs['WITHOUT']:
            s_after = s_after - {e
                                 for role in self.kwargs['WITHOUT']
                                 for e in s_after
                                 # (role == e[3]) = compsite direct assiment
                                 # (role == e[2] and e[3] == '') single single assigment
                                 if (role == e[4]) or (role == e[3] and e[4] == '')
                                 }
        return [{sys:s_before},{sys:s_after}]

from Libs.Back.Sap.misc import Misc as misc
from Libs.Back.misc import Misc as m_

from Libs.Back.Sap.Role.Client.roles import Roles as rs_
from Libs.Back.Sap.Profile.profiles import Profiles as ps_

from Sod.models.obj_comb import Obj_comb as oc_
from Tcd_Usage.models.usage import Usage as u_

class Users():

    SEGREGATION = {
        # get the profils
        'AUTHORIZATION': ['AUTHORIZATION',
                           'UST04',
                           ['BNAME', 'PROFILE']],
        # get the roles
        'ROLE': ['ROLE',
                  'AGR_USERS',
                  ['UNAME', 'AGR_NAME', 'COL_FLAG']],
        # get the fullname
        'FULLNAME': ['FULLNAME',
                      'V_USERNAME',
                      ['BNAME', 'NAME_TEXT']],
        # get the locking status
        'LOCK_STATUS': ['LOCK_STATUS',
                        'USR02',
                        ['BNAME', 'UFLAG']],
        # get the licences
        'LICENCE': ['LICENCE',
                     'USR06',
                     ['BNAME', 'LIC_TYPE']],
        # get the gegining date of validity
        'DATE_FROM': ['DATE_FROM',
                      'USR02',
                      ['BNAME', 'GLTGV']],
        # get the ending date of validity
        'DATE_TO': ['DATE_TO',
                    'USR02',
                    ['BNAME', 'GLTGB']],
        # get the usergroups
        'USERGROUP': ['USERGROUP',
                      'USR02',
                      ['BNAME', 'CLASS']],
        # get the users
        'USER': ['USER',
                  'USR02',
                  ['BNAME', 'BNAME']],
        # get the user type
        'US_TYPE': ['US_TYPE',
                     'USR02',
                     ['BNAME', 'USTYP']],
        'PERSNUMBER': ['PERSNUMBER',
                        'V_USERNAME',
                        ['BNAME', 'PERSNUMBER']],
        # get the creator account
        'CREATOR': ['CREATOR',
                     'USR02',
                     ['BNAME', 'ANAME']],
        # get the creation date
        'CREATION_DATE': ['CREATION_DATE',
                           'USR02',
                           ['BNAME', 'TRDAT']],
        'MODIFICATOR':['MODIFICATOR',
                        'USRSTAMP',
                        ['MODIFIER', 'USERNAME','MODDATE','MODTIME']],
        # get the email address
        'EMAIL': ['EMAIL',
                   'ADR6',
                   ['PERSNUMBER', 'SMTP_ADDR']],
        # get the user parameters
        'PARAMETER': ['PARAMETER',
                       'USR05',
                       ['BNAME', 'PARID', 'PARVA']],

        'DEPARTMENT': ['DEPARTMENT',
                        'ADCP',
                        ['PERSNUMBER', 'DEPARTMENT']],

        'FUNCTION': ['FUNCTION',
                      'ADCP',
                      ['PERSNUMBER', 'FUNCTION']],

        'ALIAS': ['ALIAS',
                  'USREFUS',
                  ['BNAME', 'USERALIAS']],


    }

    def __init__(self, dd_sys=dict):
        """
        Initialisation of users
        :parameter : ld_sys (dictionnary list for pyrfc connection)
        """
        self.dd_sys = dd_sys
        self.REFUSERS = m_().do_dict_str(
            [m_().list_insert(e,
                              sys,
                              1)
             for sys in self.dd_sys
             for e in misc().read_table(self.dd_sys[sys],
                                        **{'QUERY_TABLE': 'USREFUS',
                                           'FIELDS': ['BNAME','REFUSER'],
                                           }
                                        )
             if e[-1]

             ], 2)

    def get(self, d= None, **kwargs):
        if not d:
            d = dict()
        """
        """
        for key in kwargs:
            if key == 'ASSIGNMENTS':
                d = self.assigments(d, **kwargs)
            elif key == 'UNUSED_ASSIGNMENTS':
                d = self.unused_assigments(d, **kwargs)
            elif key == 'NB_AUTHORIZATIONS':
                d = self.nb_profiles(d, **kwargs)
            elif key in ['EMAIL','DEPARTMENT','FUNCTION']:
                d = self.get_with_persnumber(d,*self.SEGREGATION[key],**kwargs)
            elif key == 'SOD_OBJECTS':
                d = self.sod_obj(d, **kwargs)
            elif key == 'USAGE':
                d = self.usage(d, **kwargs)
            elif key in self.SEGREGATION:
                d = self.get_with_bname(d,
                                        *self.SEGREGATION[key],
                                        **kwargs)
            else:
                pass
        return d

    def nb_profiles(self, d, **kwargs):
        kwargs['AUTHORIZATION'] = []
        d = self.get_with_bname(d, *self.SEGREGATION['AUTHORIZATION'], **kwargs)
        {d[user].update({'NB_AUTHORIZATIONS':{sys:{len(d[user]['AUTHORIZATION'][sys])}
                                              for sys in d[user]['AUTHORIZATION']
                                              }
                         }

                        )
         for user in d
         if 'AUTHORIZATION' in d[user]
         }
        return d

    def assigments(self, d, **kwargs):
        # retreave the AUTHORIZATIONS if not asking before
        # kwargs.update({'AUTHORIZATIONS': []})
        # test = self.get_with_bname(d,self.SEGREGATION['AUTHORIZATIONS'], **kwargs)
        if not d:
            d = self.get(**{'USER':kwargs['ASSIGNMENTS']})
        for e in ['AUTHORIZATION','ROLE']:
            kwargs[e] = list()
            d = m_().dict_merge(d, self.get_with_bname(dict(d),*self.SEGREGATION[e], **{e:''}))
        roles_  = rs_(self.dd_sys).get(**{'COMPOSITION':list({e[0]
                                                              for user in d
                                                              if 'ROLE' in d[user]
                                                              for sys in d[user]['ROLE']
                                                              for e in d[user]['ROLE'][sys]
                                                              if not e[1]})})
        if roles_:
            # role treatement
            d = m_().dict_merge(d,
                                m_().do_dict_set([
                                    [user, 'ASSIGNMENTS', sys, role[0], single, prof]
                                    for user in d
                                    if 'ROLE' in d[user]
                                    for sys in d[user]['ROLE']
                                    for role in d[user]['ROLE'][sys]
                                    if role[0] in roles_
                                    if sys in roles_[role[0]]['COMPOSITION']
                                    for single in roles_[role[0]]['COMPOSITION'][sys]
                                    for prof in roles_[role[0]]['COMPOSITION'][sys][single]
                                ],
                                    5)
                                )
        # profile treatement
        d = m_().dict_merge(d,
                            m_().do_dict_set([
                                [user, 'ASSIGNMENTS', sys, '', '', profil]
                                for user in d
                                if 'AUTHORIZATION' in d[user]
                                for sys in d[user]['AUTHORIZATION']
                                for profil in {e[:10]
                                               for e in d[user]['AUTHORIZATION'][sys]} -
                                   {p
                                    for user in d
                                    if 'ASSIGNMENTS' in d[user]
                                    if sys in d[user]['ASSIGNMENTS']
                                    for c in d[user]['ASSIGNMENTS'][sys]
                                    for s in d[user]['ASSIGNMENTS'][sys][c]
                                    for p in d[user]['ASSIGNMENTS'][sys][c][s]
                                    }
                            ],
                                5)
                            )
        print('after trreatment',d)
        return d

    def unused_assigments(self, d, **kwargs):
        # return dict() if no selection
        if not kwargs['UNUSED_ASSIGNMENTS']:
            if d:
                return m_().dict_merge(d, {user:{'UNUSED_ASSIGNMENTS':{}}
                                           for user in d}
                                       )
            else:
                return {}
        # retreave the full assigment if not asked before
        if not m_().is_key('ASSIGNMENTS', d):
            d = self.assigments(d, **{'USERS':list(kwargs['UNUSED_ASSIGNMENTS'])})
        for user in set(kwargs['UNUSED_ASSIGNMENTS']) & set(d):
            if 'AUTHORIZATIONS' in d[user]:
                #{'MTAMERNI': {'SW2CLNT100': {'SU01': 8}}}
                for sys in kwargs['UNUSED_ASSIGNMENTS'][user]:
                    d_unused_role = dict()
                    if set(kwargs['UNUSED_ASSIGNMENTS'][user][sys]):
                        ps = ps_({sys: self.dd_sys[sys]})
                        it_values = [{'OBJCT': 'S_TCODE',
                                      'FIELD': 'TCD',
                                      'VAL1': e[:10]}
                                     for e in set(kwargs['UNUSED_ASSIGNMENTS'][user][sys])
                                     ]
                        # get the matching profil with the TCD usage
                        s_profiles = {prof['PROFN'][:10]
                                      for prof in ps.SUSR_SUIM_API_RSUSR020(**{
                            'IT_PROF': [{'SIGN': 'I',
                                         'OPTION': 'EQ',
                                         'LOW': e}
                                        for e in d[user]['AUTHORIZATIONS'][sys]
                                        ],
                            'IT_VALUES':it_values})[sys]}
                        # update those role with the profile witout S_TCODE Object
                        s_profiles.update({prof[:10]
                                           for prof in d[user]['AUTHORIZATIONS'][sys]
                                           }-{prof['PROFN'][:10]
                                              for prof in ps.SUSR_SUIM_API_RSUSR020(
                                                                **{'IT_PROF': [{'SIGN': 'I',
                                                                                'OPTION': 'EQ',
                                                                                'LOW': e}
                                                                               for e in d[user]
                                                                               ['AUTHORIZATIONS'][sys]
                                                                               ],
                                                                   'IT_VALUES':[{'OBJCT': 'S_TCODE',}]})[sys]
                                              })
                        for composite in d[user]['ASSIGNMENTS'][sys]:
                            if composite:
                                if not {prof[:10]
                                        for single in d[user]['ASSIGNMENTS'][sys][composite]
                                        for prof in d[user]['ASSIGNMENTS'][sys][composite][single]
                                        }.issubset(s_profiles):
                                    d_unused_role.update({composite:d[user]['ASSIGNMENTS'][sys][composite]})
                            else:
                                for single in d[user]['ASSIGNMENTS'][sys]['']:
                                    if single:
                                        if not {prof[:10]
                                                for prof in d[user]['ASSIGNMENTS'][sys][''][single]}.issubset(s_profiles):
                                            d_unused_role = m_().dict_merge(d_unused_role,
                                                                            {'':{single:
                                                                                     d[user]['ASSIGNMENTS'][sys][''][single]
                                                                                 }
                                                                             }
                                                                            )
                                    else:
                                        s_p = {prof[:10]
                                               for prof in d[user]['ASSIGNMENTS'][sys]['']['']} - s_profiles
                                        if s_p:
                                            d_unused_role = m_().dict_merge(d_unused_role,
                                                                            {'':{'':s_p
                                                                                 }
                                                                             }
                                                                            )
                    d[user]= m_().dict_merge(d[user],
                                             {'UNUSED_ASSIGNMENTS':{sys:d_unused_role}})
        for user in set(d)-set(kwargs['UNUSED_ASSIGNMENTS']):
            if 'ASSIGNMENTS' in d[user]:
                d[user] = m_().dict_merge(d[user],
                                          {'UNUSED_ASSIGNMENTS':d[user]['ASSIGNMENTS'] })
        return d

    def get_with_bname(self, d, *args, **kwargs):
        if kwargs[args[0]]:
            if d:
                return m_().dict_merge(d,
                                       m_().do_dict_set(
                                           [m_().list_insert(m_().list_insert(e,
                                                                              sys,
                                                                              1),
                                                             args[0],
                                                             1)
                                            for sys in self.dd_sys
                                            for a in [kwargs[args[0]][x:x + 1950]
                                                      for x in range(0, len(kwargs[args[0]]), 1950)
                                                      ]
                                            for e in misc().read_table(self.dd_sys[sys],
                                                                       **{'QUERY_TABLE': args[1],
                                                                          'FIELDS': args[2],
                                                                          'OPTIONS': misc().options(args[2][1],
                                                                                                    a)
                                                                          }
                                                                       )

                                            if e[0] in d], 3),
                                       )
            else:
                return m_().dict_merge(d,
                                       m_().do_dict_set(
                                           [m_().list_insert(m_().list_insert(e,
                                                                              sys,
                                                                              1),
                                                             args[0],
                                                             1)
                                            for sys in self.dd_sys
                                            for a in [kwargs[args[0]][x:x + 1950]
                                                      for x in range(0, len(kwargs[args[0]]), 1950)
                                                      ]
                                            for e in misc().read_table(self.dd_sys[sys],
                                                                       **{'QUERY_TABLE': args[1],
                                                                          'FIELDS': args[2],
                                                                          'OPTIONS': misc().options(args[2][1],
                                                                                                    a)
                                                                          }
                                                                       )

                                            ], 3),
                                       )
        else:
            if d:
                return m_().dict_merge(d,
                                       m_().do_dict_set(
                                           [m_().list_insert(m_().list_insert(e,
                                                                              sys,
                                                                              1),
                                                             args[0],
                                                             1)
                                            for sys in self.dd_sys
                                            for a in [sorted(d)[x:x + 1950]
                                                      for x in range(0, len(d), 1950)
                                                      ]
                                            for e in misc().read_table(self.dd_sys[sys],
                                                                       **{'QUERY_TABLE': args[1],
                                                                          'FIELDS': args[2],
                                                                          'OPTIONS': misc().options(args[2][0],
                                                                                                    a)
                                                                          }
                                                                       )

                                            ], 3),
                                       )
            else:
                return m_().dict_merge(d,
                                       m_().do_dict_set(
                                           [m_().list_insert(m_().list_insert(e,
                                                                              sys,
                                                                              1),
                                                             args[0],
                                                             1)
                                            for sys in self.dd_sys
                                            for e in misc().read_table(self.dd_sys[sys],
                                                                       **{'QUERY_TABLE': args[1],
                                                                          'FIELDS': args[2],
                                                                          }
                                                                       )

                                            ], 3),
                                       )

    def get_with_persnumber(self,d,*args,**kwargs):
        if not 'PERSNUMBER' in kwargs:
            kwargs['PERSNUMBER'] = []
            d = self.get_with_bname(d, *self.SEGREGATION['PERSNUMBER'], **kwargs)

        kwargs[args[0]] = []
        d_ = self.get_with_bname(m_().do_dict_set([[prsnum, 'PERSNUMBER', sys, prsnum]
                                                   for user in d
                                                   if 'PERSNUMBER' in d[user]
                                                   for sys in d[user]['PERSNUMBER']
                                                   for prsnum in d[user]['PERSNUMBER'][sys]
                                                   ], 3),
                                 *args,
                                 **kwargs)
        {d[user].update(m_().do_dict_set([[args[0],sys,val]
                                          for sys in d[user]['PERSNUMBER']
                                          for prsnum in d[user]['PERSNUMBER'][sys]
                                          if prsnum in d_
                                          if args[0] in d_[prsnum]
                                          if sys in d_[prsnum][args[0]]
                                          for val in d_[prsnum][args[0]][sys]
                                          ],2))
         for user in d
         if 'PERSNUMBER' in d[user]
         }
        return d

    def sod_obj(self, d, **kwargs):
        if not 'ASSIGNMENTS' in kwargs:
            d = self.get(d, **{'ASSIGNMENTS':list()})
        return oc_.sod.user_obj_active(d)

    def change(self, *args, **kwargs):
        return {user:{sys:misc().launch_fm(self.dd_sys[sys],*args[0],**kwargs[user][sys])
                      for sys in kwargs[user]
                      if sys in self.dd_sys
                      }
                for user in kwargs
                }

    def usage(self, d, **kwargs):
        return m_().dict_merge(d,
                               u_.usage.get(**kwargs['USAGE'])
                               )






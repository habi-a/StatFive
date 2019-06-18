from Libs.Back.Sap.misc import Misc as ms_
from Libs.Back.misc import Misc as m_
from Sod.models.obj_comb import Obj_comb as oc_

from datetime import date


class Roles():

    SEGREGATION = {
        'ROLE': ['ROLE',
                 'AGR_DEFINE',
                 ['AGR_NAME']
                 ],
        'COLLECTIVE': ['COLLECTIVE',
                       'AGR_FLAGS',
                       ['AGR_NAME', 'FLAG_VALUE'],
                       [["FLAG_TYPE EQ 'COLL_AGR' AND FLAG_VALUE EQ 'X'"],
                        ["AND (FLAG_TYPE EQ 'COLL_AGR' AND FLAG_VALUE EQ 'X')"]]
                       ],
        'PARENT': ['PARENT',
                   'AGR_DEFINE',
                   ['PARENT_AGR','AGR_NAME'],
                   [["(PARENT_AGR NE '')"],
                    ["AND (PARENT_AGR NE '')"]]
                   ],
        'DERIVED': ['DERIVED',
                    'AGR_DEFINE',
                    ['AGR_NAME','PARENT_AGR'],
                    [["(PARENT_AGR NE '')"],
                     ["AND (PARENT_AGR NE '')"]]
                    ],
        'PROFIL': ['PROFIL',
                   'AGR_1016',
                   ['AGR_NAME', 'PROFILE']
                   ],
        'DESCRIPTION': ['DESCRIPTION',
                        'AGR_TEXTS',
                        ['AGR_NAME','TEXT'],
                        [["(LINE EQ '0' AND SPRAS EQ '%s')" ],
                         ["AND (LINE EQ '0' AND SPRAS EQ '%s')"]]
                        ],
        'AGR_AGRS': ['AGR_AGRS',
                     'AGR_AGRS',
                     ['AGR_NAME', 'CHILD_AGR']
                     ],
    }

    def __init__(self,dd_sys=None):
        self.dd_sys = dd_sys

    def get(self,d=None, lang ='EN', **kwargs):
        if not d:
            d = dict()
        for arg in kwargs:
            if arg == 'SIMPLE':
                d = self.simple(dict(d), **kwargs)
            elif arg == 'COMPOSITION':
                d = self.composition(dict(d), **kwargs)
            elif arg == 'SOD_OBJECTS':
                d = self.sod_objects(dict(d), **kwargs)
            elif arg in self.SEGREGATION:
                d = self.get_with_agr_name(dict(d),
                                           lang,
                                           *self.SEGREGATION[arg],
                                           **kwargs)
            else:
                pass
        return d

    def simple(self, d, **kwargs):
        d_ = self.get(**{'COLLECTIVE':kwargs['SIMPLE'],
                         'PARENT':kwargs['SIMPLE'],
                         'DERIVED':kwargs['SIMPLE'],
                         })
        return m_().dict_merge(d,m_().do_dict_set([[role,'SIMPLE',sys,'X']
                                                   for sys in self.dd_sys
                                                   for role in  set(kwargs['SIMPLE'])-set(r
                                                                                          for r in d_
                                                                                          for type_ in d_[r]
                                                                                          if sys in d_[r][type_]
                                                                                          )],
                                                  3)
                               )

    def composition(self, d, **kwargs):
        d_ = self.get(**{'PARENT': kwargs['COMPOSITION']})
        d_ = m_().dict_merge(dict(d_), self.get(**{'DERIVED': kwargs['COMPOSITION']}))
        d_ = m_().dict_merge(dict(d_), self.get(**{'COLLECTIVE': kwargs['COMPOSITION']}))
        d_ = m_().dict_merge(dict(d_), self.get(**{'SIMPLE': kwargs['COMPOSITION']}))
        a_ = ''
        if [role
            for role in d_
            if 'COLLECTIVE' in d_[role]]:
                a_ = self.get(**{'AGR_AGRS': [role
                                              for role in d_
                                              if 'COLLECTIVE' in d_[role]]})
        p_ = self.get(**{'PROFIL': [role
                                    for compo in a_
                                    for sys in a_[compo]['AGR_AGRS']
                                    for role in a_[compo]['AGR_AGRS'][sys]]+
                                   [role
                                    for role in d_
                                    if 'COLLECTIVE' not in d_[role]
                                    ]

                         }
                      )
        for role in d_:
            for t in d_[role]:
                if t == 'COLLECTIVE':
                    d = m_().dict_merge(dict(d),
                                        m_().do_dict_set(
                                        [[role,'COMPOSITION',sys,r,prof]
                                         for sys in d_[role]['COLLECTIVE']
                                         if role in a_
                                         if 'AGR_AGRS' in a_[role]
                                         if sys in a_[role]['AGR_AGRS']
                                         for r in a_[role]['AGR_AGRS'][sys]
                                         if r in p_
                                         if 'PROFIL' in p_[r]
                                         if sys in p_[r]['PROFIL']
                                         for prof in p_[r]['PROFIL'][sys]
                                         ]
                                        ,4))
                else:
                    d = m_().dict_merge(dict(d),
                                        m_().do_dict_set([[role, 'COMPOSITION', sys, '', profil]
                                                          for sys in d_[role][t]
                                                          if role in p_
                                                          if sys in p_[role]['PROFIL']
                                                          for profil in {prof
                                                                         for prof in p_[role]['PROFIL'][sys]}
                                                          ]
                                                         , 4)
                                        )
        return d

    def sod_objects(self, d, **kwargs):
        if not m_().is_key('COMPOSITION',d):
            d = m_().dict_merge(dict(d),self.get(**{'COMPOSITION':kwargs['SOD_OBJECTS'] if kwargs['SOD_OBJECTS'] else ''}))
        return oc_.sod.role_obj_active(dict(d))

    def get_with_agr_name(self, d, lang, *args, **kwargs):
        if len(args)>3 and '%s' in str(args[3]):
            for x in range(len(args[3])):
                args[3][x][0] = args[3][x][0]%lang.upper()
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
                                            for e in ms_().read_table(self.dd_sys[sys],
                                                                      **{'QUERY_TABLE': args[1],
                                                                         'FIELDS': args[2],
                                                                         'OPTIONS': ms_().options(args[2][1],
                                                                                                  a)+args[3][1] if len(args)>3 else ['']
                                                                         }
                                                                      )

                                            #if e[0] in d
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
                                            for a in [kwargs[args[0]][x:x + 1950]
                                                      for x in range(0, len(kwargs[args[0]]), 1950)
                                                      ]
                                            for e in ms_().read_table(self.dd_sys[sys],
                                                                      **{'QUERY_TABLE': args[1],
                                                                         'FIELDS': args[2],
                                                                         'OPTIONS': ms_().options(args[2][0],
                                                                                                  a)+args[3][1] if len(args)>3 else ['']
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
                                            for e in ms_().read_table(self.dd_sys[sys],
                                                                      **{'QUERY_TABLE': args[1],
                                                                         'FIELDS': args[2],
                                                                         'OPTIONS': ms_().options(args[2][0],
                                                                                                  a)+args[3][1] if len(args)>3 else ['']
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
                                            for e in ms_().read_table(self.dd_sys[sys],
                                                                      **{'QUERY_TABLE': args[1],
                                                                         'FIELDS': args[2],
                                                                         'OPTIONS': args[3][0] if len(args)>3 else ['']
                                                                         }
                                                                      )

                                            ], 3),
                                       )

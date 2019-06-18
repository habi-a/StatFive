from django.views import View

from django.shortcuts import render

from django.utils.translation import get_language

from django.conf.urls import url

from django.utils.decorators import method_decorator

from django.contrib.messages import get_messages

from django.contrib.auth.decorators import login_required

from rest_framework.response import Response

from Test.models import Tmp_Analysis
from Libs.Back.misc import Misc as m_
from Libs.Back.User.users import Users as us_
from Libs.Back.Sap.misc import Misc as ms_
from Sod.models import Risk as risk
from Sod.models import Fun as fun
from Basis.models import Description as desc
from Libs.Front.CBV.decorators import user_is_authorized
from Libs.Front.Forms.charfield import c
from Libs.Front.Forms.datefield import d
from Libs.Front.Forms.filefield import f
from Libs.Front.Forms.filefield import fs
from Libs.Front.Forms.selectfield import s
from Libs.Front.Forms.selectfield import sm
from Libs.Front.Forms.charfield import t

from django.utils.translation import ugettext as _

from Basis.models import Sys_Type
from Basis.models import User_Details

from django.forms import formset_factory
from rest_framework.views import APIView


class Libs:
    SEGREGATION = {'ACCNT': ['ACCNT',
                             'USR02',
                             ['ACCNT']],
                   'KOSTL': ['KOSTL',
                             'USR21',
                             ['KOSTL']],
                   'USERGROUP': ['USERGROUP',
                                 'USR02',
                                 ['CLASS']],
                   'DEPARTMENT': ['DEPARTMENT',
                                  'ADCP',
                                  ['DEPARTMENT']],
                   'FUNCTION': ['FUNCTION',
                                'ADCP',
                                ['FUNCTION']],
                   'US_TYPE': ['US_TYPE',
                               'USR02',
                               ['USTYP']],
                   'LICENCE': ['LICENCE',
                               'USR06',
                               ['LIC_TYPE']],
                   'ROLE': ['ROLE',
                            'AGR_DEFINE',
                            ['AGR_NAME']],
                   'RISK': ['Sod',
                            risk,
                            ['r']],
                   '_FUNCTION': ['Sod',
                                 fun,
                                 ['f']],
                   'USER':['USER',
                           us_,
                           ['FULLNAME']]

                   }

    def _get(self, data):
        d = dict()
        for key in data['ON']:
            if key in ['RISK', '_FUNCTION']:
                d_desc = desc.d.by_content_type(lang=get_language()[0].upper(),
                                                app=self.SEGREGATION[key][0].split('_')[0],
                                                model=self.SEGREGATION[key][1].__name__)
                d[key] = {'data': [{"id": e, "value": "%s : %s - %s" % (d_desc[key] if key in d_desc else key,
                                                                        e,
                                                                        d_desc[e] if e in d_desc else _('No description')), "name": e}
                                   for e in [e[self.SEGREGATION[key][2][0]]
                                             for e in self.SEGREGATION[key][1].objects.all().values(self.SEGREGATION[key][2][0])
                                             ]]
                          }
            elif key in ['USER']:
                d[key] = {'data':[{"id": e[0], "value":"%s : %s (%s)" % (e[-2], e[0], e[-1]), "name": e[0]}
                                  for e in m_().dict_2_list(self.SEGREGATION[key][1](data['SYS']).get({},
                                                                                                      **{self.SEGREGATION[key][2][0]:[]}))
                                  ]
                          }

            elif key in self.SEGREGATION:
                d_desc = desc.d.parameters_fields(lang=get_language()[0].upper())
                d[key] = {'data':[{"id": e.split('|')[1], "value":"%s : %s" % tuple(e.split('|')), "name": e.split('|')[1]}
                                  for e in list(set(sys+'|'+e
                                                    for sys in data['SYS']
                                                    for e in ms_().read_table(m_().get_sys_info(sys),
                                                                              **{'QUERY_TABLE': self.SEGREGATION[key][1],
                                                                                 'FIELDS': self.SEGREGATION[key][2]
                                                                                 }
                                                                              )
                                                    )
                                                )]}

        return Response(d,
                        status=200,
                        template_name=None,
                        content_type="application/json")


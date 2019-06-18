from Libs.Back.Sap.misc import Misc as ms_
from Libs.Back.misc import Misc as m_
from Libs.Back.Sap.Matrix.update import Update as u_

from Libs.Back.Sap.Profile.profiles import Profiles as ps_

from Sod.models import Obj_comb

from time import sleep
from threading import Thread as th


class Qualification():

    def __init__(self,sys):
        self.sys = sys
        self.d_ = dict()

    def qualification(self):
        self.profils_qualification()
        self.get_descriptions()

    def profils_qualification(self):
        d_obj = Obj_comb.sod.qualification(**{'sys': self.sys})
        if not d_obj:
            return
        l_obj = sorted(d_obj)
        for x in range(0,len(l_obj),5):
            try:
                a = th(None,
                       self.get_profs,
                       None,
                       ({l_obj[x]:set(d_obj[l_obj[x]])},),
                       None)
                a.start()
                a = th(None,
                       self.get_profs,
                       None,
                       ({l_obj[x+1]:set(d_obj[l_obj[x+1]])},),
                       None)
                a.start()
                a = th(None,
                       self.get_profs,
                       None,
                       ({l_obj[x+2]:set(d_obj[l_obj[x+2]])},),
                       None)
                a.start()
                a = th(None,
                       self.get_profs,
                       None,
                       ({l_obj[x+3]:set(d_obj[l_obj[x+3]])},),
                       None)
                a.start()
                a = th(None,
                       self.get_profs,
                       None,
                       ({l_obj[x+4]:set(d_obj[l_obj[x+4]])},),
                       None)
                a.start()
                a.join()
            except:pass

        sleep(15)
        u_(self.sys).qualification(self.d_)

    def get_profs(self,d):
        for obj in d:
            self.d_[obj] = {profn['PROFN'][:10]
                            for profn in ps_({self.sys:m_().get_sys_info(self.sys)}).SUSR_SUIM_API_RSUSR020(
                **{'IT_VALUES':[{'OBJCT':e.split('|')[0],
                                 'FIELD':e.split('|')[1],
                                 'VAL1':e.split('|')[2]}
                                for e in d[obj]
                                ]
                   }
            )[self.sys]
                            }
        from django.db import connections
        connections.close_all()

    def get_descriptions(self):

        u_(self.sys).description(
            **{'data':m_().do_dict_str(ms_().read_table(m_().get_sys_info(self.sys),
                                                        **{'QUERY_TABLE':'TSTCT',
                                                           'OPTIONS' : ["SPRSL IN ('FR','EN')"],
                                                           'FIELDS':['TCODE','SPRSL','TTEXT']})
                                       ,2),
               'model':'value',
               'app_label':'Sod'}
        )
        u_(self.sys).description(
            **{'data':m_().do_dict_str(ms_().read_table(m_().get_sys_info(self.sys),
                                                        **{'QUERY_TABLE':'TACTT',
                                                           'OPTIONS' : ["SPRAS IN ('FR','EN')"],
                                                           'FIELDS':['ACTVT','SPRAS','LTEXT']})
                                       ,2),
               'model':'value',
               'app_label':'Sod'}
        )
        u_(self.sys).description(
            **{'data': m_().do_dict_str(ms_().read_table(m_().get_sys_info(self.sys),
                                                         **{'QUERY_TABLE': 'T582S',
                                                            'OPTIONS': ["SPRSL IN ('FR','EN')"],
                                                            'FIELDS': ['INFTY', 'SPRSL', 'ITEXT']})
                                        , 2),
               'model': 'value',
               'app_label': 'Sod'}
        )
        # ===================================================
        u_(self.sys).description(
            **{'data':m_().do_dict_str(ms_().read_table(m_().get_sys_info(self.sys),
                                                        **{'QUERY_TABLE':'TOBJT',
                                                           'OPTIONS' : ["LANGU IN ('FR','EN')"],
                                                           'FIELDS':['OBJECT','LANGU','TTEXT']})
                                       ,2),
               'model':'object',
               'app_label':'Sod'}
        )
        #-------------------------------------------------------

        authx = m_().do_dict_set(ms_().read_table(m_().get_sys_info(self.sys),
                                                  **{'QUERY_TABLE':'AUTHX',
                                                     'FIELDS':['ROLLNAME','FIELDNAME']}
                                                  )
                                 )
        for x in range(0,len(authx),1500):
            di_ = m_().do_dict_str(ms_().read_table(m_().get_sys_info(self.sys),
                                                   **{'QUERY_TABLE': 'DD04V',
                                                      'OPTIONS': ms_().options("ROLLNAME",
                                                                               list(authx)[x:x + 1500],
                                                                               *["AND DDLANGUAGE IN ('FR','EN')"]
                                                                               ),
                                                      'FIELDS': ['ROLLNAME', 'DDLANGUAGE', 'DDTEXT']})
                                  ,2)


            u_(self.sys).description(
                **{'data': {fieldname:di_[key]
                            for key in di_
                            if key in authx
                            for fieldname in authx[key]},
                   'model': 'field',
                   'app_label': 'Sod'}
            )
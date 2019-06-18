from pyrfc import *

from datetime import date
from datetime import timedelta
from datetime import datetime

from Libs.Back.misc import Misc as m
from Libs.Back.Sap.misc import Misc as ms

import random

import string

import time

class Job():

    def __init__(self, sys, program ,lang = 'EN'):
        self.d_sys = m().get_sys_info(sys)
        self.program = program
        self.lang = lang
        self.status = ''
        self.jobname = program[:32]
        self.jobcount = ''
        self.variant = ''
        self.spool_id = ''
        
    def add_variant(self,**kwargs):
        """
        Method for creating a variante in SAP
        Kwargs available =  VARI_CONTENTS
        return the variante name
        """
        if kwargs and 'VARI_CONTENTS' in kwargs:
            kwargs = {e : kwargs[e]
                      for e in kwargs
                      if e in ['VARI_CONTENTS']}
            variant = 'Z_'
            # auto generation of the variant name
            for x in range(12):
                variant = variant + random.choice(string.ascii_uppercase)
            self.variant = variant
            dict_ = {'CURR_REPORT' : self.program,
                     'CURR_VARIANT' : variant,
                     'VARI_DESC' : {'REPORT': self.program,
                                    'VARIANT': self.variant,
                                    'TRANSPORT':'F',
                                    'ENVIRONMNT':'A',
                                    'ENAME': self.d_sys['user'],
                                    'MLANGU': self.lang},
                     'VARI_TEXT' : [{'MANDT': self.d_sys['client'],
                                     'LANGU': self.lang,
                                     'REPORT': self.program,
                                     'VARIANT': self.variant,
                                     'VTEXT': self.variant}]
                     }
            kwargs.update(dict_)
            return ms().launch_fm(self.d_sys,
                                 'RS_CREATE_VARIANT_RFC',
                                 **kwargs)['RETURN']['MESSAGE']


    def delete_variant(self):
        if self.variant:
            ms().launch_fm(self.d_sys,
                          'RS_VARIANT_DELETE_RFC',
                          **{'REPORT' : self.program,
                             'VARIANT' : self.variant,}
                          )['RETURN']['MESSAGE']

    def get_job_status(self,cpt):
        """
        Checks whether a job is still running and waits until it completes.
        :param jobname:
        :param jobcount:
        """
        a = ms().read_table(self.d_sys,
                            **{'QUERY_TABLE' : 'TBTCO',
                              'FIELDS' : ['STATUS'],
                              'OPTIONS' : ["JOBNAME EQ '%s' AND JOBCOUNT EQ '%s'"%(self.jobname,
                                                                                   self.jobcount)]
                              })[0]
        if cpt == 3600:
            with Connection(**self.d_sys) as bapi:
                bapi.call('BAPI_XMI_LOGON',
                          EXTCOMPANY='SWING',
                          EXTPRODUCT='SWING',
                          INTERFACE='XBP',#obligatoire pour le lancement en Batch
                          VERSION='2.0')#obligatoire pour le lancement en Batch
                bapi.call('BAPI_XBP_JOB_ABORT',
                          JOBNAME = self.jobname,
                          JOBCOUNT = self.jobcount,
                          EXTERNAL_USER_NAME = self.d_sys['user']
                          )
                          
            
        if a not in ['F','A']: # F >> OK, A >> NOK
            time.sleep(1)
            cpt+=1
            self.get_job_status(cpt)
        else:
            self.status = a
            self.get_spool_id()            

    def launch(self):
        #Generetion of the job name in shown in SAP SM37
        with Connection(**self.d_sys) as bapi:
            bapi.call('BAPI_XMI_LOGON',
                      EXTCOMPANY='SWING',
                      EXTPRODUCT='SWING',
                      INTERFACE='XBP',#obligatoire pour le lancement en Batch
                      VERSION='2.0')#obligatoire pour le lancement en Batch
            
            self.jobcount = bapi.call('BAPI_XBP_JOB_OPEN',
                                      JOBNAME=self.jobname,
                                      EXTERNAL_USER_NAME=self.d_sys['user']
                                      )['JOBCOUNT']

            bapi.call('BAPI_XBP_JOB_ADD_ABAP_STEP',
                      JOBNAME = self.jobname,
                      JOBCOUNT = self.jobcount,
                      EXTERNAL_USER_NAME = self.d_sys['user'],
                      ABAP_PROGRAM_NAME = self.program,
                      ABAP_VARIANT_NAME = self.variant
                      )

            bapi.call('BAPI_XBP_JOB_CLOSE',
                      JOBNAME = self.jobname,
                      JOBCOUNT = self.jobcount,
                      EXTERNAL_USER_NAME = self.d_sys['user'])

            bapi.call('BAPI_XBP_JOB_START_ASAP',
                      JOBNAME = self.jobname,
                      JOBCOUNT = self.jobcount,
                      EXTERNAL_USER_NAME = self.d_sys['user'])

    def get_spool_id(self):
        self.spool_id = int(ms().read_table(self.d_sys,
                                            **{'QUERY_TABLE':'TBTCP',
                                               'FIELDS': ['LISTIDENT'],
                                               'OPTIONS' : ["JOBNAME EQ '%s' AND "%self.jobname,
                                                            "JOBCOUNT EQ '%s'"%self.jobcount]}
                                            )[0]
                            )

    def get_spool(self):
        self.get_job_status(0)
        if self.spool_id:
            with Connection(**self.d_sys) as bapi:
                bapi.call('BAPI_XMI_LOGON',
                          EXTCOMPANY='SWING',
                          EXTPRODUCT='SWING',
                          INTERFACE='XBP',#obligatoire pour le lancement en Batch
                          VERSION='2.0')#obligatoire pour le lancement en Batch
                return bapi.call('BAPI_XBP_JOB_READ_SINGLE_SPOOL',
                                            SPOOL_REQUEST=self.spool_id,
                                            EXTERNAL_USER_NAME=self.d_sys['user']
                                            )['SPOOL_LIST_PLAIN']
        else:
            return []
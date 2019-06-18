from Basis.models import Sys_Type as s

from Libs.misc import Misc as m

from Libs.Sap.misc import Misc as ms

from Sod.models import Profil_orga

class Orga():

    def __init__(self,l_sys):
        self.l_sys = l_sys
        self.BUKRS = self.get_bukrs()
        self.WERKS = self.get_werks()
        self.VKORG = self.get_vkorg()

    def profil_orga(self):
        """
        Get all the profil orga by sys qualified from ld_sys
        """
        # get the orga value qualification form the database
        return m().do_dict_set([[e['system'],
                                 e['Profil'],
                                 e['Code_auto'],
                                 e['Field_orga'],
                                 e['Value_orga']]
                                for e in Profil_orga.objects.filter(system__in = [e
                                                                                  for e in self.l_sys]).values('system','Profil',
                                                                                                                'Code_auto','Field_orga',
                                                                                                                'Value_orga')]
                               ,4)

    def get_bukrs(self):
        """
        Get all company code existing from ld_sys
        """
        d = dict()
        for sys in self.l_sys:
            if s.objects.filter(system = sys).values_list('type_sys', flat = True) == ['SAP']:
                d[sys] = ms().read_table(m().get_sys_info(sys),
                                                       **{'QUERY_TABLE':'T001',
                                                          'FIELDS':['BUKRS']}
                                                       )
        return d

    def get_werks(self):
        """
        Get all plant existing from l_sys
        """
        d = dict()
        for sys in self.l_sys:
            if s.objects.filter(system = sys).values_list('type_sys', flat = True) == ['SAP']:
                bwkey = {e[0]:e[1]
                         for e in ms().read_table(m().get_sys_info(sys),
                                                  **{'QUERY_TABLE':'T001K',
                                                     'FIELDS':['BWKEY',
                                                               'BUKRS',]}
                                     )
                         }
                d[sys] = {e[1]:{'BUKRS':bwkey[e[0]],
                                              'VKORG':e[-1]}
                                        for e in ms().read_table(m().get_sys_info(sys),
                                                                 **{'QUERY_TABLE':'T001W',
                                                                    'FIELDS':['BWKEY',
                                                                              'WERKS',
                                                                              'VKORG']}
                                                                 )
                                        }
        return d

    def get_vkorg(self):
        """
        Get all Sales organization existing from l_sys
        """
        d = dict()
        for sys in self.l_sys:
            if s.objects.filter(system = sys).values_list('type_sys', flat = True) == ['SAP']:
                d[sys] =  {e[1]:{'BUKRS':e[0],
                                               'WERKS':e[-1]}
                                         for e in ms().read_table(m().get_sys_info(sys),
                                                                  **{'QUERY_TABLE':'TVKO',
                                                                     'FIELDS':['BUKRS',
                                                                               'VKORG',
                                                                               'WERKS']}
                                                                  )
                                         }
        return d

    

    

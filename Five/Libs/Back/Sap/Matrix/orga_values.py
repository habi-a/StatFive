from Libs.Sap.misc import Misc as ms
from Libs.misc import Misc as m


class Orga_values():

    def __init__(self,l_sys):
        self.ld_sys = [m().get_sys_info(sys)
                       for sys in l_sys]

    def get_bukrs(self):
        d = dict()
        for d_sys in self.ld_sys:
            d[d_sys['sys_name']] = ms().read_table(d_sys,
                                                   **{'QUERY_TABLE':'T001',
                                                      'FIELDS':['BUKRS']}
                                                   )
        return d

    def get_werks(self):
        d = dict()
        for d_sys in self.ld_sys:
            bwkey = {e[0]:e[1]
                     for e in ms().read_table(d_sys,
                                              **{'QUERY_TABLE':'T001K',
                                                 'FIELDS':['BWKEY',
                                                           'BUKRS',]}
                                 )
                     }
            d[d_sys['sys_name']] = {e[1]:{'BUKRS':bwkey[e[0]],
                                          'VKORG':e[-1]}
                                    for e in ms().read_table(d_sys,
                                                             **{'QUERY_TABLE':'T001W',
                                                                'FIELDS':['BWKEY',
                                                                          'WERKS',
                                                                          'VKORG']}
                                                             )
                                    }
        return d

    def get_vkorg(self):
        d = dict()
        for d_sys in self.ld_sys:
            d[d_sys['sys_name']] =  {e[1]:{'BUKRS':e[0],
                                           'WERKS':e[-1]}
                                     for e in ms().read_table(d_sys,
                                                              **{'QUERY_TABLE':'TVKO',
                                                                 'FIELDS':['BUKRS',
                                                                           'VKORG',
                                                                           'WERKS']}
                                                              )
                                     }
        return d

    def get_valueorg(self):
        d = dict()        
        d['WERKS'] = self.get_werks()
        d['VKORG'] = self.get_vkorg()
        d['BUKRS'] = self.get_bukrs()
        '''
        for sys in bukrs:
            for bukr in bukrs[sys]:
                try:
                    d['BUKRS'][sys].update({bukr:{'WERKS': {werks
                                                            for werks in d['WERKS'][sys]
                                                            if bukr == d['WERKS'][sys][werks]['BUKRS']},
                                                  'VKORG': {vkorg
                                                            for vkorg in d['VKORG'][sys]
                                                            if bukr == d['VKORG'][sys][vkorg]['BUKRS']}
                                                  }
                                            })
                except:
                    try:
                        d['BUKRS'].update({sys:{bukr:{'WERKS': {werks
                                                            for werks in d['WERKS'][sys]
                                                            if bukr == d['WERKS'][sys][werks]['BUKRS']},
                                                      'VKORG': {vkorg
                                                                for vkorg in d['VKORG'][sys]
                                                                if bukr == d['VKORG'][sys][vkorg]['BUKRS']}
                                                      }
                                                }
                                           }
                                          )
                    except:
                        d['BUKRS'] = {sys:{bukr:{'WERKS': {werks
                                                           for werks in d['WERKS'][sys]
                                                           if bukr == d['WERKS'][sys][werks]['BUKRS']},
                                                 'VKORG': {vkorg
                                                           for vkorg in d['VKORG'][sys]
                                                           if bukr == d['VKORG'][sys][vkorg]['BUKRS']}
                                                 }
                                           }
                                      }
        '''
        return d
        
        
        


        

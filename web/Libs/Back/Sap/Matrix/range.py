from pyrfc import *

from Libs.Back.misc import Misc as m_
from Libs.Back.Sap.misc import Misc as ms_



class Range():

    def __init__(self,sys):
        self.d_sys = m_().get_sys_info(sys)

    def range(self, dict_):
        # va chercher dans SAP les valeurs des possible des ranges
        # si pas range sur autre que ACTVT, incremente en BASE 36 et prend toutes les valeurs
        # a revoir pour InfoType.
        for tcd in dict_:
            for obj in dict_[tcd]:
                li = []
                for val in dict_[tcd][obj]:
                    # only one value 
                    if val[1]:
                        if 'ACTVT' in obj:
                            li.extend(ms_().read_table(self.d_sys,**{'QUERY_TABLE':'TACTZ',
                                                                     'FIELDS':['ACTVT'],
                                                                     'OPTIONS':["BROBJ = '%s' AND ACTVT BETWEEN '%s' AND '%s'"%(obj.split('|')[0],
                                                                                                                                val[0],
                                                                                                                                val[1])]
                                                                     }
                                                       )
                                      )
                        elif 'INFTY' in obj:
                            li.extend(ms_().read_table(self.d_sys,**{'QUERY_TABLE':'T582S',
                                                                     'FIELDS':['INFTY'],
                                                                     'OPTIONS':["SPRSL = 'D' AND INFTY BETWEEN '%s' AND '%s'" %(val[0],val[1])]
                                                                     }
                                                       )
                                      )
                            
                        else:
                            li.extend([m_().base36encode(x,len(val[1]))
                                       for x in range(m_().base36decode(val[0]),
                                                      m_().base36decode(val[1])+1,
                                                      1)
                                       ])
                    else:
                        li.append(val[0])
                dict_[tcd][obj] = sorted(li)
        return dict_

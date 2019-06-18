from Libs.Analysis.orga import Orga as _

from collections import defaultdict as dd

class Orga(_):

    def __init__(self,l_sys):
        super().__init__(l_sys)


    def get_profil_orga_qual(self):
        d_prof_orga = self.profil_orga()

        
        d_orga = vars(self)
        d_orga.pop('l_sys')
        # dict key creation  for 
        d_ = dd(set)
        for sys in d_prof_orga:
            for prof in d_prof_orga[sys]:
                for auth in d_prof_orga[sys][prof]:
                    for field in d_prof_orga[sys][prof][auth]:
                        if field in d_orga:
                            if sys in d_orga[field]:
                                for value in d_prof_orga[sys][prof][auth][field]:
                                    if value in d_orga[field][sys]:
                                        if field == 'BUKRS':
                                            d_['%s%s%s'%(sys,auth,prof)].add((value,'',''))
                                        elif field == 'WERKS':
                                            d_['%s%s%s'%(sys,auth,prof)].add((d_orga[field][sys][value]['BUKRS'],
                                                                              value,
                                                                              d_orga[field][sys][value]['VKORG']))
                                        else:
                                            d_['%s%s%s'%(sys,auth,prof)].add((d_orga[field][sys][value]['BUKRS'],
                                                                              d_orga[field][sys][value]['WERKS'],
                                                                              value
                                                                              ))
        return d_
        


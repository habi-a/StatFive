from Sod.models import Risque as risk_

from Libs.misc import Misc as misc_

class Risks():

    def __init__(self):
        pass

    def risks(self):
        return misc_().do_dict_set([[e['Risque'],e['Fonction']]
                                   for e in risk_.objects.values()])

    def get_activated_risks(self,set_):
        """
        Give the activated function form d_fun
        """
        ##################################################
        ###
        ### A intégrer la notion d'identité si les comptes 
        ### users diffèrent d'une appli à l'autre
        ###
        ##################################################
        
        # no function activated
        if not set_:
            return set()
        d_risks = self.risks()
        s_risks = set()
        d_fun = misc_().do_dict_set(list(set_),2)
        s_risks.update({tuple(list(e)[::-1]+[risk])
                        for key in d_fun
                        for risk in  d_risks
                        if d_risks[risk].issubset(set(d_fun[key]))
                        for fun in d_risks[risk]
                        for e in d_fun[key][fun]
                        })
        return s_risks

    def risk_impact(self,d_risk):
        """
        d like {BEFORE:set(),AFTER:()}
        return a dict
                    [KEPT] = {(KEY,RISK)}
                    [REMOVED] = {(KEY,RISK)}
                    [ADDED] = {(KEY,RISK)}
        """
        set_before = {(e[0],e[-1]) for e in d_risk['BEFORE']}
        set_after = {(e[0],e[-1]) for e in d_risk['AFTER']}
        d = dict()
        d['KEPT'] = set_before & set_after # intersect between both sets
        d['REMOVED'] = set_before - set_after # in set_before and not in set_after
        d['ADDED'] = set_after - set_before # in set_after and not in set_before
        return d

        
        
        

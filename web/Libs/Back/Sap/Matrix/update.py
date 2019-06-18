from Sod.models import *
import sys
from Basis.models import Sys_Type, Description

from django.contrib.contenttypes.models import ContentType

class Update():

    def __init__(self, sys = ''):
        self.sys = sys

    def function_update(self,functions): 
        s_obj = set(Obj.objects.values_list(flat = True))
        Obj.objects.bulk_create([Obj(o = e)
                                 for e in {val
                                           for function in functions
                                           for tcd in functions[function]
                                           for comb_tcd in functions[function][tcd]
                                           for obj in functions[function][tcd][comb_tcd]
                                           for val in set(functions[function][tcd][comb_tcd][obj] - s_obj)
                                           
                                           }
                                 ])
        
        d_Obj_comb = dict()
        for function in functions:
            f,aaa = Fun.objects.get_or_create(f = function)
            for tcd in functions[function]:
                for comb_tcd in functions[function][tcd]:
                    sf,aaa = Sfun.objects.get_or_create(sf = '%s|%s'%(tcd,comb_tcd))
                    f.sfs.add(sf)
                    for obj in functions[function][tcd][comb_tcd]:
                        obj_comb = tuple(sorted(functions[function][tcd][comb_tcd][obj]))
                        if obj in d_Obj_comb:
                            if obj_comb in d_Obj_comb[obj]:                                    
                                pass
                            else:
                                d_Obj_comb[obj].update({obj_comb:obj+'|%s'%len(d_Obj_comb[obj])})
                        else:
                            d_Obj_comb.update({obj:
                                               {obj_comb:
                                                obj+'|0'}})
                        cmb,aaa = Obj_comb.objects.get_or_create(oc = d_Obj_comb[obj][obj_comb])
                        cmb.sys.add(self.sys)
                        cmb.os.set(obj_comb)
                        sf.ocs.add(cmb)

    def qualification(self,dict_):
        for obj in dict_:
            s_op = set()
            for prof in dict_[obj]:
                p,v = Prof.objects.get_or_create(p=prof)
                op,v = Prof_sys.objects.get_or_create(p = p,
                                                      sys = Sys_Type(self.sys))
                s_op.add(op)
            obj_ = Obj_comb.objects.get(oc = obj)
            s_ps = set(Obj_comb.objects.filter(**{'oc':obj,
                                                  'ps__sys':self.sys}
                                               ).values_list('ps'))
            #for deleting
            [obj_.ps.remove(e)
             for e in s_ps - s_op]
            #for updating
            [obj_.ps.add(e)
             for e in s_op - s_ps]

    def description(self,**kwargs):
        for key in kwargs['data']:
            key_ ,v = getattr(sys.modules[__name__],
                              kwargs['model'].capitalize()
                              ).objects.get_or_create(**{kwargs['model'][0]:key})
            if v:
                a = ContentType.objects.get(app_label= kwargs['app_label'],
                                            model=kwargs['model'],
                                            )
                for lang in kwargs['data'][key]:
                    Description.objects.create(content_object = a.get_object_for_this_type(**{kwargs['model'][0]:key}),
                                               lang= lang,
                                               desc = kwargs['data'][key][lang]
                                               )


    

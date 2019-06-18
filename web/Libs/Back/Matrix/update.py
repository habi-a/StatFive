from Sod.models import *
from django.contrib.contenttypes.models import ContentType
from Libs.Back.misc import Misc as m_
from Basis.models.description import Description

import sys


class Update():

    def risk(self,file):
        #suppression des ligne à 1 et ajout en masse des objets S_TCODE
        file = ''.join([chunk.decode("utf-8") for chunk in file.chunks()])

        d_ = {z[0]:list(z[1:])
              for z in {tuple([i for i in e.split(';')[:6] if i])
                        for e in file.split('\r\n')
                        }
              if z}
        
        for risk in d_:
            r,v = Risk.objects.get_or_create(r = risk)
            for fun in d_[risk]:
                f,v = Fun.objects.get_or_create(f = fun)
                r.fs.add(f)

        d_ = m_().do_dict_set(list({(z[-1],z[0])
                                    for z in {tuple([i for i in e.split(';')[:7] if i])
                                              for e in file.split('\r\n')
                                              }
                                     if z})
                                   )

        for dom in d_:
            rt,v = Risk_Type.objects.get_or_create(rt = dom)
            for risk in d_[dom]:
                r,v = Risk.objects.get_or_create(r = risk)
                rt.rs.add(r)

    def description(self,**kwargs):
        lines = m_().do_dict_str(list({tuple(e.split(';'))
                                      for e in ''.join([chunk.decode("latin-1") for chunk in kwargs['file'].chunks()]).split('\r\n')
                                      if e
                                      }
                                     )
                                ,2)
        a = ContentType.objects.get(app_label= kwargs['app_label'],
                                    model=kwargs['model'],
                                    )
        for key in set(lines)&set(getattr(sys.modules[__name__],
                                          kwargs['model'].capitalize()
                                          ).objects.values_list(kwargs['model'][0],flat = True)
                                  ):

            for lang in lines[key]:

                Description.objects.create(content_object = a.get_object_for_this_type(**{kwargs['model'][0]:key}),
                                           lang= lang,
                                           desc = lines[key][lang]
                                           )

            
        
                                
                                
        
                
            
        

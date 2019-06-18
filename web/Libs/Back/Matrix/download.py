from Basis.models import Sys_Type
from Libs.Back.Sap.Matrix.file import Matrix as sm_
from Libs.Back.misc import Misc as m_
from Libs.Back.Matrix.update import Update as u_


class Matrix_Import():
    """
    Class importing matrix
    """
    
    def __init__(self,sys = ''):
        self.sys = sys
        
    def function(self,fichier):
        if 'SAP' == Sys_Type.objects.filter(system = self.sys).values_list('type_sys')[0][0]:
            sm_(self.sys).function(fichier)


    def risk(self,fichier):
        u_().risk(fichier)
            

    def function_description(self,fichier):
        u_().description(**{'file':fichier,
                            'app_label':'Sod',
                            'model':'fun'})
        '''
        lines = m_().do_dict_str(list({tuple(e.split(';'))
                 for e in ''.join([chunk.decode("latin-1") for chunk in fichier.chunks()]).split('\r\n')
                 if e
                 })
                                 ,2)
        f_ = ContentType.objects.get(app_label= 'Sod',
                                     model="fun",
                                     )
        for fun_ in lines:
            for lang in lines[fun_]:
                Description.objects.create(content_object = f_.get_object_for_this_type(f = fun_),
                                           lang= lang,
                                           desc = lines[fun_][lang]
                                           )
        '''

    def risk_description(self,fichier):
        u_().description(**{'file':fichier,
                            'app_label':'Sod',
                            'model':'risk'})
        '''
        lines = m_().do_dict_str(list({tuple(e.split(';'))
                 for e in ''.join([chunk.decode("latin-1") for chunk in fichier.chunks()]).split('\r\n')
                 if e
                 })
                                 ,2)
        a = ContentType.objects.get(app_label= 'Sod',
                                    model="risk",
                                    )
        for r_ in set(lines)&set(Risk.objects.values_list('r',flat = True)):
            for lang in lines[r_]:
                Description.objects.create(content_object = a.get_object_for_this_type(r = r_),
                                           lang= lang,
                                           desc = lines[r_][lang]
                                           )
        '''



                
                    
                    
                
            
    
                        



    


    

        

from Libs.Back.Sap.Matrix.range import Range as r_
from Libs.Back.Sap.Matrix.update import Update as u_

from Libs.Back.misc import Misc as m_


class Matrix():

    def __init__(self,sys):
        self.sys = sys
    
    def function(self,file):
        #suppression des ligne à 1 et ajout en masse des objets S_TCODE
        f = ''.join([chunk.decode("utf-8") for chunk in file.chunks()])
        lines = {tuple(e.split(';')[:-2])
                  for e in f.split('\r\n')
                  if e.split(';')[-1] == '0'}

        lines.update({(e.split(';')[0].strip(),
                     e.split(';')[1].strip(),
                     'S_TCODE',
                     'TCD',
                     e.split(';')[1].strip(),
                     '')
                    for e in f.split('\r\n')
                    })
        # lines like {('MM09', 'MIAV', 'S_ARCHIVE', 'ACTVT', '02', '')...}
        d_matrix = dict()
        for e in lines:
            if e[0] in d_matrix:
                if e[1] in d_matrix[e[0]]:
                    if e[2]+'|'+e[3] in d_matrix[e[0]][e[1]]:
                        d_matrix[e[0]][e[1]][e[2]+'|'+e[3]].add(e[-2:])
                    else:
                        d_matrix[e[0]][e[1]].update({e[2]+'|'+e[3]:{e[-2:]}})
                else:
                    d_matrix[e[0]].update({e[1]:
                                               {e[2]+'|'+e[3]:
                                                {e[-2:]}}})                    
            else:
                d_matrix[e[0]] = {e[1]:{e[2]+'|'+e[3]:{e[-2:]}}}
        for fun in d_matrix:
            d_matrix[fun] = r_(self.sys).range(d_matrix[fun])
        
        for fun in d_matrix:
            for tcd in d_matrix[fun]:
                d_matrix[fun][tcd] = self.matricial_product(tcd, d_matrix[fun][tcd])
        u_(self.sys).function_update(d_matrix)

    def matricial_product(self, tcd, dict_):
        if 'F110' in tcd:
            dict_.update({'F_REGU_BUK|FBTCH':
                               ['02','11','12','14','15','21','24','25','26','31']})

            if tcd == 'F110S':
                dict_.update({'S_PROGRAM|P_ACTION':['SUBMIT']})
                dict_.update({'S_PROGRAM|P_GROUP':['F_001']})
            li = list()
            for obj in dict_:
                li.append(['%s|%s'%(obj,val)
                               for val in dict_[obj]
                               ])
            li = self.F110(sorted(li), tcd)

            
        else:
            li = list()   
            for obj in dict_:
                li.append(['%s|%s'%(obj,val)
                           for val in dict_[obj]
                           ])
            li = m_().produit_matriciel(li)
        '''
        [dict_.__setitem__(str(x),li[x])
         for x in range(len(li))]
        '''
        return {str(x):self.obj_grouping(li[x])
                for x in range(len(li))}
            
    def F110(self,liste,option):
        for x in range(len(liste)):
            liste[x]=sorted(liste[x])
        if option=='F110':
            return [[liste[0][z],
                     liste[1][z],
                     liste[2][0]]
                    for z in range(len(liste[0]))]
        else:
            return [[liste[0][z],
                     liste[1][z],
                     liste[2][0],
                     liste[3][0],
                     liste[4][0],]
                    for z in range(len(liste[0]))]

    def obj_grouping(self, liste):
        s_ = [e[:e.find('|')]
              for e in liste]
        dict_ = dict()
        [dict_.__setitem__(obj,{val})
         if obj not in dict_
         else
         dict_[obj].add(val)
         for obj in s_
         for val in liste
         if obj == val[:len(obj)]]
        return dict_


                
                

        
        
        
        

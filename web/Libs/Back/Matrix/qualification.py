from Basis.models import Sys_Type
from Sod.models import Risk

from Libs.Back.Sap.Matrix.qualification import Qualification as qs_


class Qualification():

    def __init__(self):
        pass

    def get_systems(self):
        return Sys_Type.objects.values('system','type_sys')

    def qualification(self):
        for sys in self.get_systems():
            if sys['type_sys'] == 'SAP':
                qs_(sys['system']).qualification()

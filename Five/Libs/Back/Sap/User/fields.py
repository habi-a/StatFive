from Libs.Sap.misc import Misc as misc

from Libs.misc import Misc as m

class Fields():

    def __init__(self, sys):
        self.d_sys =  m().get_sys_info(sys)

    def get_fields(self):
        fields = ['BAPILOGOND','BAPIPWD','BAPIDEFAUL','BAPIADDR3',
                  'BAPIUSCOMP','BAPISNCU','BAPIREFUS','BAPIALIAS']
        return [['USERNAME',None]] + misc().read_table(
            self.d_sys,
            **{'QUERY_TABLE':'DD03L',
               'OPTIONS' : ["TABNAME EQ '%s'"%fields[x]
                            if x == len(fields)-1
                            else
                            "TABNAME EQ '%s' OR"%fields[x]
                            for x in range(len(fields))],
               'FIELDS':['FIELDNAME','TABNAME']}
            )
            

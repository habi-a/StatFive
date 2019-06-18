class Abap():

    def get_auths_with_spec_vals(self,body):
        # program initialisation
        header = [{'LINE':"REPORT Z_ORGA_PROF."},
                  # declaration table interne des auths
                  {'LINE':"DATA: BEGIN OF  authlist OCCURS 10."},
                  {'LINE':"INCLUDE STRUCTURE usreflangu."},
                  {'LINE':"DATA: END OF authlist."},
                  # declaration table interne des values for selection
                  {'LINE':"DATA: BEGIN OF  values OCCURS 10."},
                  {'LINE':"INCLUDE STRUCTURE usreflangu."},
                  {'LINE':"DATA: END OF values."},
                  # creation of another table interne
                  {'LINE':"DATA matrix_values LIKE TABLE OF values."},]
        #End program
        footer = [{'LINE':"CALL FUNCTION 'SUSR_GET_AUTHS_WITH_SPEC_VALS'"},
                  {'LINE':"EXPORTING"},
                  {'LINE':"SRCHTYPE = 'AND'"},
                  {'LINE':"AKTPS = 'A'"},
                  {'LINE':"TABLES"},
                  {'LINE':"VALUES = matrix_values"},
                  {'LINE':"AUTHS = authlist."},
                  {'LINE':"APPEND values TO matrix_values."},
                  # retreave the result in ['WRITES']
                  {'LINE':"LOOP AT authlist."},
                  {'LINE':"write:/ authlist-auth."},
                  {'LINE':"ENDLOOP."},]
        
        #filing the internal table will be done in the fonction 
        return header + body + footer

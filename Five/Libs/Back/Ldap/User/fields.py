from ldap3 import *

import ssl

from Libs.misc import Misc as m

class Fields():

     def __init__(self,sys):
         """
        Class for managing Users in LDAP
        input dict with the connection info
        self.base = base of LADP tree
        self.sys_name = sys_name of ldap
        self.d_sys = conection info to LDAP
        """
        sys = m().get_sys_info(sys)
        self.base = sys.pop('base')
        self.sys_name = sys.pop('sys_name')
        self.d_sys = sys
        tls_configuration = Tls(validate=ssl.CERT_REQUIRED,
                                version=ssl.PROTOCOL_TLSv1)
        # Free ipa Case has to be removed for customer
        tls_configuration.validate = ssl.CERT_NONE
        self.d_sys['server'] = Server(self.d_sys['server'],
                                      tls = tls_configuration)


    def get_fields(self):
        """
        Method for getting the attribute for inetorgperson
        return list of attribute
        """
        with Connection(**self.d_sys) as ad:
            return {self.sys_name : sorted([(attr.__dict__['name'],'')
                                            for attr in ObjectDef('inetorgperson', ad)
                                            if attr.__dict__['name'] != 'objectClass'])}

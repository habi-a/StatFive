from Libs.Back.misc import Misc as m
from Libs.Back.Sap.misc import Misc as misc


class Role():

    def __init__(self,role,sys):
        """
        Class for role matter
        role = str
        d_sys = dict for SAP connection
        """
        self.role = role
        self.d_sys = m().get_sys_info(sys)

    def exist(self):
        """
        get all the profiles for a roles
        param self.role
        return  = boolean or Error
        """
        return misc().fm_bool_info(misc().read_table(self.d_sys,
                                                 **{'QUERY_TABLE':'AGR_DEFINE',
                                                    'OPTIONS' : ["AGR_NAME EQ '%s'"%self.role],
                                                    'FIELDS': ['AGR_NAME']}
                                                 )
                                 )

    def get_profiles(self):
        """
        get all the profiles for a roles
        param self.role
        return  = {sys : {profiles} or Error}
        """
        if self.is_compo():
            roles = self.get_compo()
            options = ["AGR_NAME EQ '%s'"%roles[x].upper()
                       if x == len(roles)-1
                       else
                       "AGR_NAME EQ '%s' OR"%roles[x].upper()
                       for x in range(len(roles))
                       ]
        else:
            options =  ["AGR_NAME EQ '%s'"%self.role]
        s_profiles = misc().read_table(self.d_sys,
                                     **{'QUERY_TABLE':'AGR_1016',
                                        'OPTIONS' : options,
                                        'FIELDS': ['PROFILE']}
                                     )
        if isinstance(s_profiles,str):
             return s_profiles
        else:
             return set(s_profiles)

    def is_parent(self):
        """
        param self.role
        return  = boolean or Error
        """
        return misc().fm_bool_info(misc().read_table(self.d_sys,
                                                 **{'QUERY_TABLE':'AGR_DEFINE',
                                                    'OPTIONS' : ["PARENT_AGR EQ '%s'"%self.role],
                                                    'FIELDS': ['AGR_NAME']}
                                                 )
                                 )

    def is_derived(self):
        """
        param self.role
        return  = boolean or Error
        """
        return misc().fm_bool_info(misc().read_table(self.d_sys,
                                                 **{'QUERY_TABLE':'AGR_DEFINE',
                                                    'OPTIONS' : ["AGR_NAME EQ '%s'"%self.role],
                                                    'FIELDS': ['PARENT_AGR']}
                                                 )
                                 )
    
    def is_compo(self):
        """
        param self.role
        return  = boolean or Error
        """
        return misc().fm_bool_info(misc().read_table(self.d_sys,
                                                 **{'QUERY_TABLE':'AGR_FLAGS',
                                                    'OPTIONS' : ["AGR_NAME EQ '%s' AND"%self.role,
                                                                 "FLAG_TYPE EQ 'COLL_AGR' AND FLAG_VALUE EQ 'X'"],
                                                    'FIELDS': ['AGR_NAME']}
                                                 )
                                 )

    def is_single(self):
        """
        param self.role
        return  = boolean or Error
        """
        existence = self.exist()
        # forcing false if the role doesn't exist
        if (existence,str):
            return existence
        if self.is_parent() == self.is_derived() == self.is_compo():
            return True
        else:
            return False

    def get_parent(self):
        """
        param self.role
        return  = parent or Error
        """
        if self.is_derived():
            return misc().read_table(self.d_sys,
                                   **{'QUERY_TABLE':'AGR_DEFINE',
                                      'OPTIONS' : ["AGR_NAME EQ '%s'"%self.role],
                                      'FIELDS': ['PARENT_AGR']}
                                   )
        else:
            return None

    def get_compo(self):
        """
        Get the composite role liked if the role is not a collective agr
        else get the composition of the composite role
        param self.role
        return  = parent or Error
        """
        # if is collective agr
        if self.is_compo():
            return misc().read_table(self.d_sys,
                                   **{'QUERY_TABLE':'AGR_AGRS',
                                      'OPTIONS' : ["AGR_NAME EQ '%s'"%self.role],
                                      'FIELDS': ['CHILD_AGR']}
                                      )
        else:
            return misc().read_table(self.d_sys,
                                   **{'QUERY_TABLE':'AGR_AGRS',
                                      'OPTIONS' : ["CHILD_AGR EQ '%s'"%self.role],
                                      'FIELDS': ['AGR_NAME']}
                                      )

    def get_derived(self):
        """
        Get the composite role liked if the role is not a collective agr
        else get the composition of the composite role
        param self.role
        return  = parent or Error
        """
        # if is a parent agr > give all the reived roles
        if self.is_parent():
            return misc().read_table(self.d_sys,
                                   **{'QUERY_TABLE':'AGR_DEFINE',
                                      'OPTIONS' : ["PARENT_AGR EQ '%s'"%self.role],
                                      'FIELDS': ['AGR_NAME']}
                                      )
        # if is derived get all the derived role form the same parent agr
        elif self.is_derived():
            return misc().read_table(self.d_sys,
                                     **{'QUERY_TABLE':'AGR_DEFINE',
                                        'OPTIONS' : ["PARENT_AGR EQ '%s'"%self.get_parent()[0]],
                                        'FIELDS': ['AGR_NAME']}
                                     )
        # if is a sigle or a composite role return itself
        else:
            return [self.role]

    
